"""Deprecated module."""
from __future__ import annotations

import importlib
import sys
import warnings


warnings.filterwarnings(action="once", category=ImportWarning)

warnings.warn(
    message=f"The '{__name__}' module has been deprecated; import from '{__package__}' instead",
    category=ImportWarning,
    stacklevel=2,
)

sys.modules[__name__] = importlib.import_module(__package__)
