"""Module for parsing text files.."""
from typing import Iterator

from promptmanager.script.base.document_loaders.base import BaseBlobParser
from promptmanager.script.base.document_loaders.blob_loaders import Blob
from promptmanager.script.base.schema import Document


class TextParser(BaseBlobParser):
    """Parser for text blobs."""

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """Lazily parse the blob."""
        yield Document(page_content=blob.as_string(), metadata={"source": blob.source})
