"""**Retriever** class returns Documents given a text **query**.

It is more general than a vector store. A retriever does not need to be able to
store documents, only to return (or retrieve) it. Vector stores can be used as
the backbone of a retriever, but there are other types of retrievers as well.

**Class hierarchy:**

.. code-block::

    BaseRetriever --> <name>Retriever  # Examples: ArxivRetriever, MergerRetriever

**Main helpers:**

.. code-block::

    Document, Serializable, Callbacks,
    CallbackManagerForRetrieverRun, AsyncCallbackManagerForRetrieverRun
"""

from promptmanager.script.base.retrievers.arxiv import ArxivRetriever
from promptmanager.script.base.retrievers.azure_cognitive_search import AzureCognitiveSearchRetriever
from promptmanager.script.base.retrievers.bm25 import BM25Retriever
from promptmanager.script.base.retrievers.chaindesk import ChaindeskRetriever
from promptmanager.script.base.retrievers.chatgpt_plugin_retriever import ChatGPTPluginRetriever
from promptmanager.script.base.retrievers.contextual_compression import ContextualCompressionRetriever
from promptmanager.script.base.retrievers.docarray import DocArrayRetriever
from promptmanager.script.base.retrievers.elastic_search_bm25 import ElasticSearchBM25Retriever
from promptmanager.script.base.retrievers.ensemble import EnsembleRetriever
from promptmanager.script.base.retrievers.google_cloud_enterprise_search import (
    GoogleCloudEnterpriseSearchRetriever,
)
from promptmanager.script.base.retrievers.google_vertex_ai_search import (
    GoogleVertexAISearchRetriever,
)
from promptmanager.script.base.retrievers.kay import KayAiRetriever
from promptmanager.script.base.retrievers.kendra import AmazonKendraRetriever
from promptmanager.script.base.retrievers.knn import KNNRetriever
from promptmanager.script.base.retrievers.llama_index import (
    LlamaIndexGraphRetriever,
    LlamaIndexRetriever,
)
from promptmanager.script.base.retrievers.merger_retriever import MergerRetriever
from promptmanager.script.base.retrievers.metal import MetalRetriever
from promptmanager.script.base.retrievers.milvus import MilvusRetriever
from promptmanager.script.base.retrievers.multi_query import MultiQueryRetriever
from promptmanager.script.base.retrievers.multi_vector import MultiVectorRetriever
from promptmanager.script.base.retrievers.parent_document_retriever import ParentDocumentRetriever
from promptmanager.script.base.retrievers.pinecone_hybrid_search import PineconeHybridSearchRetriever
from promptmanager.script.base.retrievers.pubmed import PubMedRetriever
from promptmanager.script.base.retrievers.re_phraser import RePhraseQueryRetriever
from promptmanager.script.base.retrievers.remote_retriever import RemotePMRetriever
from promptmanager.script.base.retrievers.self_query.base import SelfQueryRetriever
from promptmanager.script.base.retrievers.svm import SVMRetriever
from promptmanager.script.base.retrievers.tavily_search_api import TavilySearchAPIRetriever
from promptmanager.script.base.retrievers.tfidf import TFIDFRetriever
from promptmanager.script.base.retrievers.time_weighted_retriever import (
    TimeWeightedVectorStoreRetriever,
)
from promptmanager.script.base.retrievers.vespa_retriever import VespaRetriever
from promptmanager.script.base.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever
from promptmanager.script.base.retrievers.web_research import WebResearchRetriever
from promptmanager.script.base.retrievers.wikipedia import WikipediaRetriever
from promptmanager.script.base.retrievers.zep import ZepRetriever
from promptmanager.script.base.retrievers.zilliz import ZillizRetriever

__all__ = [
    "AmazonKendraRetriever",
    "ArxivRetriever",
    "AzureCognitiveSearchRetriever",
    "ChatGPTPluginRetriever",
    "ContextualCompressionRetriever",
    "ChaindeskRetriever",
    "ElasticSearchBM25Retriever",
    "GoogleCloudEnterpriseSearchRetriever",
    "GoogleVertexAISearchRetriever",
    "KayAiRetriever",
    "KNNRetriever",
    "LlamaIndexGraphRetriever",
    "LlamaIndexRetriever",
    "MergerRetriever",
    "MetalRetriever",
    "MilvusRetriever",
    "MultiQueryRetriever",
    "PineconeHybridSearchRetriever",
    "PubMedRetriever",
    "RemotePMRetriever",
    "SVMRetriever",
    "SelfQueryRetriever",
    "TavilySearchAPIRetriever",
    "TFIDFRetriever",
    "BM25Retriever",
    "TimeWeightedVectorStoreRetriever",
    "VespaRetriever",
    "WeaviateHybridSearchRetriever",
    "WikipediaRetriever",
    "ZepRetriever",
    "ZillizRetriever",
    "DocArrayRetriever",
    "RePhraseQueryRetriever",
    "WebResearchRetriever",
    "EnsembleRetriever",
    "ParentDocumentRetriever",
    "MultiVectorRetriever",
]
