"""**Embedding models**  are wrappers around embedding models
from different APIs and services.

**Embedding models** can be LLMs or not.

**Class hierarchy:**

.. code-block::

    Embeddings --> <name>Embeddings  # Examples: OpenAIEmbeddings, HuggingFaceEmbeddings
"""


import logging
from typing import Any

from promptmanager.script.base.embeddings.aleph_alpha import (
    AlephAlphaAsymmetricSemanticEmbedding,
    AlephAlphaSymmetricSemanticEmbedding,
)
from promptmanager.script.base.embeddings.awa import AwaEmbeddings
from promptmanager.script.base.embeddings.baidu_qianfan_endpoint import QianfanEmbeddingsEndpoint
from promptmanager.script.base.embeddings.bedrock import BedrockEmbeddings
from promptmanager.script.base.embeddings.cache import CacheBackedEmbeddings
from promptmanager.script.base.embeddings.clarifai import ClarifaiEmbeddings
from promptmanager.script.base.embeddings.cohere import CohereEmbeddings
from promptmanager.script.base.embeddings.dashscope import DashScopeEmbeddings
from promptmanager.script.base.embeddings.deepinfra import DeepInfraEmbeddings
from promptmanager.script.base.embeddings.edenai import EdenAiEmbeddings
from promptmanager.script.base.embeddings.elasticsearch import ElasticsearchEmbeddings
from promptmanager.script.base.embeddings.embaas import EmbaasEmbeddings
from promptmanager.script.base.embeddings.ernie import ErnieEmbeddings
from promptmanager.script.base.embeddings.fake import DeterministicFakeEmbedding, FakeEmbeddings
from promptmanager.script.base.embeddings.google_palm import GooglePalmEmbeddings
from promptmanager.script.base.embeddings.gpt4all import GPT4AllEmbeddings
from promptmanager.script.base.embeddings.gradient_ai import GradientEmbeddings
from promptmanager.script.base.embeddings.huggingface import (
    HuggingFaceBgeEmbeddings,
    HuggingFaceEmbeddings,
    HuggingFaceInferenceAPIEmbeddings,
    HuggingFaceInstructEmbeddings,
)
from promptmanager.script.base.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
from promptmanager.script.base.embeddings.javelin_ai_gateway import JavelinAIGatewayEmbeddings
from promptmanager.script.base.embeddings.jina import JinaEmbeddings
from promptmanager.script.base.embeddings.llamacpp import LlamaCppEmbeddings
from promptmanager.script.base.embeddings.localai import LocalAIEmbeddings
from promptmanager.script.base.embeddings.minimax import MiniMaxEmbeddings
from promptmanager.script.base.embeddings.mlflow_gateway import MlflowAIGatewayEmbeddings
from promptmanager.script.base.embeddings.modelscope_hub import ModelScopeEmbeddings
from promptmanager.script.base.embeddings.mosaicml import MosaicMLInstructorEmbeddings
from promptmanager.script.base.embeddings.nlpcloud import NLPCloudEmbeddings
from promptmanager.script.base.embeddings.octoai_embeddings import OctoAIEmbeddings
from promptmanager.script.base.embeddings.ollama import OllamaEmbeddings
from promptmanager.script.base.embeddings.openai import OpenAIEmbeddings
from promptmanager.script.base.embeddings.sagemaker_endpoint import SagemakerEndpointEmbeddings
from promptmanager.script.base.embeddings.self_hosted import SelfHostedEmbeddings
from promptmanager.script.base.embeddings.self_hosted_hugging_face import (
    SelfHostedHuggingFaceEmbeddings,
    SelfHostedHuggingFaceInstructEmbeddings,
)
from promptmanager.script.base.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from promptmanager.script.base.embeddings.spacy_embeddings import SpacyEmbeddings
from promptmanager.script.base.embeddings.tensorflow_hub import TensorflowHubEmbeddings
from promptmanager.script.base.embeddings.vertexai import VertexAIEmbeddings
from promptmanager.script.base.embeddings.xinference import XinferenceEmbeddings

logger = logging.getLogger(__name__)

__all__ = [
    "OpenAIEmbeddings",
    "CacheBackedEmbeddings",
    "ClarifaiEmbeddings",
    "CohereEmbeddings",
    "ElasticsearchEmbeddings",
    "HuggingFaceEmbeddings",
    "HuggingFaceInferenceAPIEmbeddings",
    "GradientEmbeddings",
    "JinaEmbeddings",
    "LlamaCppEmbeddings",
    "HuggingFaceHubEmbeddings",
    "MlflowAIGatewayEmbeddings",
    "ModelScopeEmbeddings",
    "TensorflowHubEmbeddings",
    "SagemakerEndpointEmbeddings",
    "HuggingFaceInstructEmbeddings",
    "MosaicMLInstructorEmbeddings",
    "SelfHostedEmbeddings",
    "SelfHostedHuggingFaceEmbeddings",
    "SelfHostedHuggingFaceInstructEmbeddings",
    "FakeEmbeddings",
    "DeterministicFakeEmbedding",
    "AlephAlphaAsymmetricSemanticEmbedding",
    "AlephAlphaSymmetricSemanticEmbedding",
    "SentenceTransformerEmbeddings",
    "GooglePalmEmbeddings",
    "MiniMaxEmbeddings",
    "VertexAIEmbeddings",
    "BedrockEmbeddings",
    "DeepInfraEmbeddings",
    "EdenAiEmbeddings",
    "DashScopeEmbeddings",
    "EmbaasEmbeddings",
    "OctoAIEmbeddings",
    "SpacyEmbeddings",
    "NLPCloudEmbeddings",
    "GPT4AllEmbeddings",
    "XinferenceEmbeddings",
    "LocalAIEmbeddings",
    "AwaEmbeddings",
    "HuggingFaceBgeEmbeddings",
    "ErnieEmbeddings",
    "JavelinAIGatewayEmbeddings",
    "OllamaEmbeddings",
    "QianfanEmbeddingsEndpoint",
]


# TODO: this is in here to maintain backwards compatibility
class HypotheticalDocumentEmbedder:
    def __init__(self, *args: Any, **kwargs: Any):
        logger.warning(
            "Using a deprecated class. Please use "
            "`from promptmanager.script.base.chains import HypotheticalDocumentEmbedder` instead"
        )
        from promptmanager.script.base.chains.hyde.base import HypotheticalDocumentEmbedder as H

        return H(*args, **kwargs)  # type: ignore

    @classmethod
    def from_llm(cls, *args: Any, **kwargs: Any) -> Any:
        logger.warning(
            "Using a deprecated class. Please use "
            "`from promptmanager.script.base.chains import HypotheticalDocumentEmbedder` instead"
        )
        from promptmanager.script.base.chains.hyde.base import HypotheticalDocumentEmbedder as H

        return H.from_llm(*args, **kwargs)
