from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional

from promptmanager.script.base.agents.agent_toolkits.base import BaseToolkit
from promptmanager.script.base.pydantic_v1 import root_validator
from promptmanager.script.base.tools import BaseTool
from promptmanager.script.base.tools.ainetwork.app import AINAppOps
from promptmanager.script.base.tools.ainetwork.owner import AINOwnerOps
from promptmanager.script.base.tools.ainetwork.rule import AINRuleOps
from promptmanager.script.base.tools.ainetwork.transfer import AINTransfer
from promptmanager.script.base.tools.ainetwork.utils import authenticate
from promptmanager.script.base.tools.ainetwork.value import AINValueOps

if TYPE_CHECKING:
    from ain.ain import Ain


class AINetworkToolkit(BaseToolkit):
    """Toolkit for interacting with AINetwork Blockchain."""

    network: Optional[Literal["mainnet", "testnet"]] = "testnet"
    interface: Optional[Ain] = None

    @root_validator(pre=True)
    def set_interface(cls, values: dict) -> dict:
        if not values.get("interface"):
            values["interface"] = authenticate(network=values.get("network", "testnet"))
        return values

    class Config:
        """Pydantic config."""

        validate_all = True
        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            AINAppOps(),
            AINOwnerOps(),
            AINRuleOps(),
            AINTransfer(),
            AINValueOps(),
        ]
