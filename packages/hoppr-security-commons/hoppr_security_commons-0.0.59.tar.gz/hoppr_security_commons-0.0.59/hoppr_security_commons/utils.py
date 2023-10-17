"""This provides a set of utility functions for working with vulnerabilities and boms."""
# This file is part of hoppr-cop
#
# Licensed under the MIT License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Copyright (c) 2022 Lockheed Martin Corporation
from __future__ import annotations

import json
import os
import stat
import tempfile
import uuid

from pathlib import Path
from typing import TYPE_CHECKING

import requests
import typer

from hoppr_cyclonedx_models.cyclonedx_1_3 import (
    CyclonedxSoftwareBillOfMaterialSpecification as Bom_1_3,
)
from hoppr_cyclonedx_models.cyclonedx_1_4 import (
    Advisory,
    Component,
    CyclonedxSoftwareBillOfMaterialsStandard as Bom_1_4,
    Reference,
    VulnerabilitySource,
)


if TYPE_CHECKING:
    from packageurl import PackageURL


def convert_xml_to_json(file_path: Path) -> Path:
    """Function to convert a xml file to json format."""
    typer.echo("xml format detected, attempt to convert with cyclonedx tools")

    # Default to the path specified in the hoppr-cop docker file or define the local filename to save data
    docker_image_path = Path("/usr/local/bin/cyclone-dx")
    cyclone_dx_path = docker_image_path if docker_image_path.exists() else Path(tempfile.gettempdir()) / "cyclonedx"
    if not cyclone_dx_path.exists():
        typer.echo("cyclonedx tools not found Attempting to download")
        if url := os.getenv("CYCLONE_INSTALL_URL"):
            # Make http request for remote file datae
            data = requests.get(url, timeout=60)

            # Save file data to local copy
            cyclone_dx_path.write_bytes(data.content)
        else:
            msg = typer.style(
                "In order to support xml boms, you must set 'CYCLONE_INSTALL_URL' to "
                "the correct release of cyclone-dx cli. https://github.com/CycloneDX/cyclonedx-cli/releases",
                fg=typer.colors.RED,
            )
            typer.echo(msg)
            raise typer.Exit(code=1)

    cyclone_dx_path.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    os.system(
        f"{cyclone_dx_path.absolute()} convert --input-file {file_path} \
            --output-file {tempfile.gettempdir()}/{file_path.name}.json --output-format json",
    )
    return Path(f"{tempfile.gettempdir()}/{file_path.name}.json")


def parse_sbom(sbom_file: Path) -> Bom_1_4 | Bom_1_3:
    """Parses a Software Bill of Materials File."""
    if sbom_file.is_file() and sbom_file.exists():
        typer.echo(f"processing {sbom_file}")

        if sbom_file.suffix == ".xml":
            sbom_file = convert_xml_to_json(sbom_file)

        sbom_json_object = json.loads(sbom_file.read_text(encoding="utf-8"))
        sbom = create_sbom_object(sbom_json_object, str(sbom_file))
    else:
        typer.secho(f"{sbom_file!s} is not a file", fg=typer.colors.RED)
        raise typer.Exit

    return sbom


def parse_sbom_json_string(sbom_file_json: str, sbom_info: str) -> Bom_1_4 | Bom_1_3:
    """Parses a Software Bill of Materials JSON String."""
    sbom_json_object = json.loads(sbom_file_json)
    return create_sbom_object(sbom_json_object, sbom_info)


def create_sbom_object(sbom_json_object: dict, sbom_info: str) -> Bom_1_4 | Bom_1_3:
    """Creates a Software Bill of Materials Object."""
    spec_version = sbom_json_object.get("specVersion", "")
    sbom_json_object.pop("$schema", None)

    sbom: Bom_1_4 | Bom_1_3
    if spec_version == "1.4":
        sbom = Bom_1_4(**sbom_json_object)
    elif spec_version == "1.3":
        sbom = Bom_1_3(**sbom_json_object)
    else:
        typer.secho(f"{sbom_info} is an unknown spec version ({spec_version})")
        raise typer.Exit

    return sbom


def get_vulnerability_source(vulnerability_id: str) -> VulnerabilitySource | None:
    """Generate the source for a vulnerability based on a given ID."""
    if vulnerability_id.startswith("CVE-"):
        return VulnerabilitySource(name="NVD", url=f"https://nvd.nist.gov/vuln/detail/{vulnerability_id}")
    if vulnerability_id.startswith("GHSA"):
        return VulnerabilitySource(name="Github Advisories", url=f"https://github.com/advisories/{vulnerability_id}")
    if vulnerability_id.startswith("GMS"):
        return VulnerabilitySource(name="Github Advisories", url=f"https://github.com/advisories/{vulnerability_id}")
    if vulnerability_id.startswith("sonatype"):
        return VulnerabilitySource(
            name="OSS Index",
            url=f"https://ossindex.sonatype.org/vulnerability/{vulnerability_id}",
        )

    return None


def get_advisories_from_urls(urls: list[str]) -> list[Advisory]:
    """Generates a list of advisories for the given set of urls."""
    urls = list(set(urls))
    return [Advisory(url=x) for x in urls]


def get_references_from_ids(ids: list[str], primary_id: str) -> list[Reference]:
    """Builds a list of Reference objects to the given vulnerability IDs."""
    references = []

    for ident in list(set(ids)):
        if ident != primary_id and (source := get_vulnerability_source(ident)):
            references.append(Reference(id=ident, source=source))

    return references


def build_bom_dict_from_purls(purls: list[PackageURL]) -> dict:
    """Create SBOM dictionary from PackageURL list."""
    sbom = Bom_1_4(specVersion="1.4", serialNumber=uuid.uuid1().urn)
    sbom.components = []  # assign explicitly for type checkers

    for purl in purls:
        component = Component(
            type="library",
            name=purl.name,
            version=purl.version,
            purl=purl.to_string(),
            group=purl.namespace,
            bom_ref=purl.to_string(),
            description="test",
            author="test",
            externalReferences=[],
        )

        sbom.components.append(component)

    return sbom.dict()


def build_bom_from_purls(purls: list[PackageURL]) -> Bom_1_4:
    """Creates a skeleton BOM from a list of purls."""
    return Bom_1_4(**build_bom_dict_from_purls(purls))
