"""Helper functions for managing the Promptmanager API.

This module is only relevant for Promptmanager developers, not for users.

.. warning::

    This module and its submodules are for internal use only.  Do not use them
    in your own code.  We may change the API at any time with no warning.

"""

from .deprecation import (
    PMDeprecationWarning,
    deprecated,
    suppress_promptmanager_deprecation_warning,
    surface_promptmanager_deprecation_warnings,
    warn_deprecated,
)

__all__ = [
    "deprecated",
    "PMDeprecationWarning",
    "suppress_promptmanager_deprecation_warning",
    "surface_promptmanager_deprecation_warnings",
    "warn_deprecated",
]
