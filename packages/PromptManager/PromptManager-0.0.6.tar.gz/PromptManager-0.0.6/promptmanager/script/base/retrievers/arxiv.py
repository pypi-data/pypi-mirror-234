from typing import List

from promptmanager.script.base.callbacks.manager import CallbackManagerForRetrieverRun
from promptmanager.script.base.schema import BaseRetriever, Document
from promptmanager.script.base.utilities.arxiv import ArxivAPIWrapper


class ArxivRetriever(BaseRetriever, ArxivAPIWrapper):
    """`Arxiv` retriever.

    It wraps load() to get_relevant_documents().
    It uses all ArxivAPIWrapper arguments without any change.
    """

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        return self.load(query=query)
