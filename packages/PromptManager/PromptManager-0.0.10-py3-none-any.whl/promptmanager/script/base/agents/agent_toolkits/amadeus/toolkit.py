from __future__ import annotations

from typing import TYPE_CHECKING, List

from promptmanager.script.base.agents.agent_toolkits.base import BaseToolkit
from promptmanager.script.base.pydantic_v1 import Field
from promptmanager.script.base.tools import BaseTool
from promptmanager.script.base.tools.amadeus.closest_airport import AmadeusClosestAirport
from promptmanager.script.base.tools.amadeus.flight_search import AmadeusFlightSearch
from promptmanager.script.base.tools.amadeus.utils import authenticate

if TYPE_CHECKING:
    from amadeus import Client


class AmadeusToolkit(BaseToolkit):
    """Toolkit for interacting with Office365."""

    client: Client = Field(default_factory=authenticate)

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            AmadeusClosestAirport(),
            AmadeusFlightSearch(),
        ]
