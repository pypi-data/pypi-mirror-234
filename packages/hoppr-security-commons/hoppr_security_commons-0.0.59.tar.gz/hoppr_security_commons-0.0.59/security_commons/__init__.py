"""
Deprecated package
"""
from __future__ import annotations

import importlib
import sys
import warnings

warnings.filterwarnings(action="once", category=ImportWarning)

warnings.warn(
    message="This package has been renamed; import from 'hoppr_security_commons' instead",
    category=ImportWarning,
)

redirect = importlib.import_module("hoppr_security_commons")

sys.modules[__name__] = redirect
sys.modules[f"{__name__}.common"] = redirect
