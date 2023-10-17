"""
**Utility functions** for Promptmanager.

These functions do not depend on any other Promptmanager module.
"""

from promptmanager.script.base.utils.env import get_from_dict_or_env, get_from_env
from promptmanager.script.base.utils.formatting import StrictFormatter, formatter
from promptmanager.script.base.utils.input import (
    get_bolded_text,
    get_color_mapping,
    get_colored_text,
    print_text,
)
from promptmanager.script.base.utils.math import cosine_similarity, cosine_similarity_top_k
from promptmanager.script.base.utils.strings import comma_list, stringify_dict, stringify_value
from promptmanager.script.base.utils.utils import (
    check_package_version,
    get_pydantic_field_names,
    guard_import,
    mock_now,
    raise_for_status_with_text,
    xor_args,
)

__all__ = [
    "StrictFormatter",
    "check_package_version",
    "comma_list",
    "cosine_similarity",
    "cosine_similarity_top_k",
    "formatter",
    "get_bolded_text",
    "get_color_mapping",
    "get_colored_text",
    "get_from_dict_or_env",
    "get_from_env",
    "get_pydantic_field_names",
    "guard_import",
    "mock_now",
    "print_text",
    "raise_for_status_with_text",
    "stringify_dict",
    "stringify_value",
    "xor_args",
]
