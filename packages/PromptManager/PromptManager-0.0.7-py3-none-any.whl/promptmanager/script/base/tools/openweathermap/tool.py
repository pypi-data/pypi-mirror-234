"""Tool for the OpenWeatherMap API."""

from typing import Optional

from promptmanager.script.base.callbacks.manager import CallbackManagerForToolRun
from promptmanager.script.base.pydantic_v1 import Field
from promptmanager.script.base.tools.base import BaseTool
from promptmanager.script.base.utilities import OpenWeatherMapAPIWrapper


class OpenWeatherMapQueryRun(BaseTool):
    """Tool that queries the OpenWeatherMap API."""

    api_wrapper: OpenWeatherMapAPIWrapper = Field(
        default_factory=OpenWeatherMapAPIWrapper
    )

    name: str = "OpenWeatherMap"
    description: str = (
        "A wrapper around OpenWeatherMap API. "
        "Useful for fetching current weather information for a specified location. "
        "Input should be a location string (e.g. London,GB)."
    )

    def _run(
        self, location: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the OpenWeatherMap tool."""
        return self.api_wrapper.run(location)
