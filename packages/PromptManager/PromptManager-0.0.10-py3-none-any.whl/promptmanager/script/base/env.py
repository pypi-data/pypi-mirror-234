import platform
from functools import lru_cache


@lru_cache(maxsize=1)
def get_runtime_environment() -> dict:
    """Get information about the Promptmanager runtime environment."""
    # Lazy import to avoid circular imports
    from promptmanager.script.base import __version__

    return {
        "library_version": __version__,
        "library": "promptmanager",
        "platform": platform.platform(),
        "runtime": "python",
        "runtime_version": platform.python_version(),
    }
