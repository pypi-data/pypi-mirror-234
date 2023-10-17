"""Provides vulnerability reporting."""
# This file is part of hoppr-security-commons
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

# Copyright (c) 2022 Lockheed Martin CorporationØ
from __future__ import annotations

import json
import uuid

from collections import defaultdict
from pathlib import Path
from typing import Any

import jinja2
import typer

from hoppr_cyclonedx_models.cyclonedx_1_4 import (
    Advisory,
    Affect,
    CyclonedxSoftwareBillOfMaterialsStandard as Bom_1_4,
    Rating,
    ScoreMethod,
    Severity,
    Vulnerability,
)
from packageurl import PackageURL
from tabulate import tabulate

from hoppr_security_commons.reporting.models import ReportFormat


class Reporting:
    """Generates reports in multiple formats from a list of vulnerabilities."""

    output_path: Path
    base_name: str

    def __init__(self, output_path: Path, base_name: str):
        self.output_path = output_path
        self.base_name = base_name

    def generate_vulnerability_reports(
        self,
        formats: list[ReportFormat],
        vulnerabilities: dict[str, list[Vulnerability] | None],
        bom: Bom_1_4 | None = None,
    ):
        """Generates various vulnerability reports based on specified formats."""
        flattened_vulnerabilties = self.__add_purl_as_bom_ref_and_flatten(vulnerabilities)

        if ReportFormat.CYCLONE_DX in formats and bom is not None:
            self.output_path.mkdir(parents=True, exist_ok=True)
            self.add_vulnerabilities_to_bom(bom, flattened_vulnerabilties)

            (self.output_path / f"{Path(self.base_name).name}-enhanced.json").write_text(
                bom.json(indent=2), encoding="utf-8"
            )

        if ReportFormat.GITLAB in formats:
            self.generate_gitlab_vulnerability_report(flattened_vulnerabilties)

        if ReportFormat.HTML in formats:
            self.__generate_html_report(flattened_vulnerabilties)

        if ReportFormat.TABLE in formats:
            findings = self.__get_fields_from_vulnerabilities(flattened_vulnerabilties)
            typer.echo(tabulate(findings, headers=["type", "name", "version", "id", "severity", "found by"]))

    @staticmethod
    def add_vulnerabilities_to_bom(bom: Bom_1_4, vulnerabilities: list[Vulnerability]) -> Bom_1_4:
        """Adds the vulnerabilities found by various scanners to cyclone 1.4+ compliant BOM."""
        if isinstance(bom, Bom_1_4):
            bom.vulnerabilities = vulnerabilities
        else:
            typer.echo("Cannot add vulnerabilities to a bom earlier than cyclone version 1.4")

        return bom

    @staticmethod
    def link_vulnerabilities_to_bom(vulnerabilities: list[Vulnerability]) -> Bom_1_4:
        """Creates/Adds the vulnerabilities found by various scanners to cyclone 1.4+ compliant VEX BOM."""
        vex_bom = Bom_1_4(bomFormat="CycloneDX", specVersion="1.4", version=1)
        vex_bom.serialNumber = f"urn:uuid:{uuid.uuid4()}"
        vex_bom.vulnerabilities = vulnerabilities

        return vex_bom

    def __add_purl_as_bom_ref_and_flatten(
        self, vulnerabilities: dict[str, list[Vulnerability] | None]
    ) -> list[Vulnerability]:
        flattened_vulnerabilities: list[Vulnerability] = []

        for purl in vulnerabilities:
            for vuln in vulnerabilities[purl] or []:
                vuln.affects = vuln.affects or []
                vuln.affects.append(Affect(ref=purl))
                flattened_vulnerabilities.append(vuln)

        flattened_vulnerabilities.sort(key=self.get_score, reverse=True)
        return flattened_vulnerabilities

    def get_score(self, vuln_to_score: Vulnerability) -> float:
        """Return best score of specified Vulnerability."""
        best_rating = self.__get_best_rating(vuln_to_score.ratings)

        if best_rating is None or best_rating.score is None:
            return 0.0

        return best_rating.score

    def __get_fields_from_vulnerabilities(self, vulnerabilities: list[Vulnerability]) -> list[list[str | None]]:
        findings = []

        def get_fields(vuln: Vulnerability) -> list[str | None]:
            tools = [f"{tool.vendor} {tool.name}" for tool in vuln.tools or []]
            severity = self.__get_severity(vuln.ratings)

            if severity == "critical":
                severity = typer.style(severity, fg=typer.colors.RED)
            elif severity == "high":
                severity = typer.style(severity, fg=typer.colors.BRIGHT_YELLOW)

            if not vulnerability.affects:
                return []

            purl = PackageURL.from_string(vulnerability.affects[0].ref)

            return [purl.type, purl.name, purl.version, vuln.id, severity, " | ".join(tools)]

        for vulnerability in vulnerabilities:
            findings.append(get_fields(vulnerability))

        return findings

    def __copy_assets(self):
        assets_dir = Path(__file__).parent / "templates" / "assets"
        assets = ["vulnerabilities.css"]

        output_path = self.output_path / "assets"
        output_path.mkdir(exist_ok=True, parents=True)

        for asset in assets:
            template_data = (assets_dir / asset).read_text(encoding="utf-8")
            (output_path / asset).write_text(template_data)

    def __generate_html_report(self, combined_list: list[Vulnerability]):
        self.output_path.mkdir(parents=True, exist_ok=True)
        output_path = self.output_path / f"{Path(self.base_name).name}-vulnerabilities.html"

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates"))
        env.filters["severity"] = self.__get_severity
        template = env.get_template("vulnerabilities.html")

        self.__copy_assets()

        severity_classes = {
            "critical": "bg-red-100 rounded-lg py-5 px-6 mb-4 text-base text-red-700 mb-3",
            "high": "bg-yellow-100 rounded-lg py-5 px-6 mb-4 text-base text-yellow-700 mb-3",
            "medium": "bg-gray-50 rounded-lg py-5 px-6 mb-4 text-base text-gray-500 mb-3",
            "info": "bg-gray-50 rounded-lg py-5 px-6 mb-4 text-base text-gray-500 mb-3",
            "low": "bg-gray-50 rounded-lg py-5 px-6 mb-4 text-base text-gray-500 mb-3",
            "unknown": "bg-gray-50 rounded-lg py-5 px-6 mb-4 text-base text-gray-500 mb-3",
            "none": "bg-gray-50 rounded-lg py-5 px-6 mb-4 text-base text-gray-500 mb-3",
        }

        result = template.render(
            {"findings": combined_list, "severity_classes": severity_classes, "base_name": self.base_name},
        )

        output_path.write_text(result, encoding="utf-8")

        self.__generate_vuln_detail_reports(combined_list, severity_classes)

    def __generate_vuln_detail_reports(self, vulnerabilities: list[Vulnerability], severity_classes: dict[str, str]):
        output_path = self.output_path / f"{Path(self.base_name).name}-details"
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates"))
        env.filters["featured_link"] = self.__get_featured_link
        template = env.get_template("vulnerability_details.html")

        for vuln in vulnerabilities:
            if not vuln.affects:
                continue

            purl = PackageURL.from_string(vuln.affects[0].ref)
            result = template.render(
                {
                    "type": purl.type,
                    "namespace": purl.namespace,
                    "name": purl.name,
                    "version": purl.version,
                    "severity_classes": severity_classes,
                    "vulnerability": vuln,
                    "purl": purl.to_string(),
                    "base_name": self.base_name,
                },
            )

            (output_path / f"{vuln.id}.html").write_text(result, encoding="utf-8")

    def generate_gitlab_vulnerability_report(self, vulnerabilities: list[Vulnerability]):
        """Renders the vulnerabilities report for gitlab."""
        # Note the JSON schema for this report can be found at
        # https://gitlab.com/gitlab-org/security-products/security-report-schemas/-/blob/master/dist/dependency-scanning-report-format.json
        report: dict[str, Any] = {
            "version": "14.1.2",
            "vulnerabilities": [],
            "remediations": [],
            "dependency_files": [],
        }

        dependencies_by_format: dict[str, list[Any]] = defaultdict(list, {})

        purls = list({vuln.affects[0].ref for vuln in vulnerabilities if vuln.affects})

        self.output_path.mkdir(parents=True, exist_ok=True)
        output_path = self.output_path / "gl-dependency-scanning-report.json"

        for purl_str in purls:
            purl = PackageURL.from_string(purl_str)
            dependencies_by_format[purl.type].append({"package": {"name": purl.name}, "version": purl.version})

        for vuln in vulnerabilities:
            report["vulnerabilities"].append(self.__generate_gitlab_row(vuln))

        for repo_format in dependencies_by_format:
            report["dependency_files"].append(
                {
                    "package_manager": repo_format,
                    "path": "cyclonedx.bom",
                    "dependencies": dependencies_by_format[repo_format],
                },
            )

        output_path.write_text(json.dumps(report, indent=4, sort_keys=True, default=str), encoding="utf-8")

    @staticmethod
    def __get_featured_link(advisories: list[Advisory] | None) -> str | None:
        if advisories is not None:
            for adv in advisories:
                url = "" if adv.url is None else adv.url
                if "https://snyk.io/" in url:
                    return url
        return None

    def __get_severity(self, ratings: list[Rating] | None) -> str:
        best_rating = self.__get_best_rating(ratings)
        if best_rating is None or best_rating.severity is None:
            return "none"

        return Severity(best_rating.severity).value

    @staticmethod
    def __get_best_rating(ratings: list[Rating] | None) -> Rating | None:
        default_rating = ratings[0] if ratings else None

        methods = [ScoreMethod(rating.method).value if rating.method else "none" for rating in ratings or []]

        preferred_method = None
        if "CVSSv31" in methods:
            preferred_method = "CVSSv31"
        elif "CVSSv3" in methods:
            preferred_method = "CVSSv3"
        elif "CVSSv2" in methods:
            preferred_method = "CVSSv2"

        return next(
            filter(lambda rating: rating.method and (str(rating.method) == preferred_method), ratings or []),
            default_rating,
        )

    def __generate_gitlab_row(self, vuln: Vulnerability) -> dict[str, Any] | None:
        """Generates a report row."""
        # Ensure `affects` and `tools` are non-empty lists
        if not vuln.affects or not vuln.tools:
            return None

        purl = PackageURL.from_string(vuln.affects[0].ref)
        severity = self.__get_severity(vuln.ratings).title()

        return {
            "category": "dependency_scanning",
            "name": vuln.description,
            "description": vuln.description,
            "cve": vuln.id,
            "severity": severity if severity != "none" else "Info",
            "confidence": "Unknown",
            "identifiers": [{"type": "cve", "name": vuln.id, "value": vuln.id}],
            "scanner": {"id": vuln.tools[0].name, "name": vuln.tools[0].name},
            "location": {
                "file": "cyclonedx.bom",
                "dependency": {"package": {"name": purl.name}, "version": purl.version},
            },
        }
