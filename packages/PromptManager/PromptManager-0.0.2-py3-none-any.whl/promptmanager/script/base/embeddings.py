from abc import ABC, abstractmethod
from typing import List


class PMEmbeddings(ABC):
    """Interface for embedding models."""

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Asynchronous Embed search docs."""
        raise NotImplementedError

    async def aembed_query(self, text: str) -> List[float]:
        """Asynchronous Embed query text."""
        raise NotImplementedError


class CohereEmbeddings(PMEmbeddings):

    def __init__(self):
        pass


class HuggingFaceEmbeddings(PMEmbeddings):
    def __init__(self):
        pass


class OpenAIEmbeddings(PMEmbeddings):
    def __init__(self):
        pass
