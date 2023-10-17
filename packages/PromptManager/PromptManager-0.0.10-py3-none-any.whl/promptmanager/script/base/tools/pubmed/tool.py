from typing import Optional

from promptmanager.script.base.callbacks.manager import CallbackManagerForToolRun
from promptmanager.script.base.pydantic_v1 import Field
from promptmanager.script.base.tools.base import BaseTool
from promptmanager.script.base.utilities.pubmed import PubMedAPIWrapper


class PubmedQueryRun(BaseTool):
    """Tool that searches the PubMed API."""

    name: str = "PubMed"
    description: str = (
        "A wrapper around PubMed. "
        "Useful for when you need to answer questions about medicine, health, "
        "and biomedical topics "
        "from biomedical literature, MEDLINE, life science journals, and online books. "
        "Input should be a search query."
    )
    api_wrapper: PubMedAPIWrapper = Field(default_factory=PubMedAPIWrapper)

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the PubMed tool."""
        return self.api_wrapper.run(query)
