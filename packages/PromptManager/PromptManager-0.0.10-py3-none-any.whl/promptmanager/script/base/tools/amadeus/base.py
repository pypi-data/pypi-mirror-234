"""Base class for Amadeus tools."""
from __future__ import annotations

from typing import TYPE_CHECKING

from promptmanager.script.base.pydantic_v1 import Field
from promptmanager.script.base.tools.amadeus.utils import authenticate
from promptmanager.script.base.tools.base import BaseTool

if TYPE_CHECKING:
    from amadeus import Client


class AmadeusBaseTool(BaseTool):
    """Base Tool for Amadeus."""

    client: Client = Field(default_factory=authenticate)
