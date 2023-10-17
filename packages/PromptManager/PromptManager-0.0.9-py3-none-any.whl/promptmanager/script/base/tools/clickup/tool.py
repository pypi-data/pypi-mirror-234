"""
This tool allows agents to interact with the clickup library
and operate on a Clickup instance.
To use this tool, you must first set as environment variables:
    client_secret
    client_id
    code

Below is a sample script that uses the Clickup tool:

```python
from promptmanager.script.base.agents import AgentType
from promptmanager.script.base.agents import initialize_agent
from promptmanager.script.base.agents.agent_toolkits.clickup.toolkit import ClickupToolkit
from promptmanager.script.base.llms import OpenAI
from promptmanager.script.base.utilities.clickup import ClickupAPIWrapper

llm = OpenAI(temperature=0)
clickup = ClickupAPIWrapper()
toolkit = ClickupToolkit.from_clickup_api_wrapper(clickup)
agent = initialize_agent(
    toolkit.get_tools(),
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```
"""
from typing import Optional

from promptmanager.script.base.callbacks.manager import CallbackManagerForToolRun
from promptmanager.script.base.pydantic_v1 import Field
from promptmanager.script.base.tools.base import BaseTool
from promptmanager.script.base.utilities.clickup import ClickupAPIWrapper


class ClickupAction(BaseTool):
    """Tool that queries the  Clickup API."""

    api_wrapper: ClickupAPIWrapper = Field(default_factory=ClickupAPIWrapper)
    mode: str
    name: str = ""
    description: str = ""

    def _run(
        self,
        instructions: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the  Clickup API to run an operation."""
        return self.api_wrapper.run(self.mode, instructions)
