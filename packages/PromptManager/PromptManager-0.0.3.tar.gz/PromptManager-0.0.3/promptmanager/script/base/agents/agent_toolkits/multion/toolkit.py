"""MultiOn agent."""
from __future__ import annotations

from typing import List

from promptmanager.script.base.agents.agent_toolkits.base import BaseToolkit
from promptmanager.script.base.tools import BaseTool
from promptmanager.script.base.tools.multion.create_session import MultionCreateSession
from promptmanager.script.base.tools.multion.update_session import MultionUpdateSession


class MultionToolkit(BaseToolkit):
    """Toolkit for interacting with the Browser Agent"""

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [MultionCreateSession(), MultionUpdateSession()]
