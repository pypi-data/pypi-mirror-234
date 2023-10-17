# ruff: noqa: E402
"""Main entrypoint into package."""
import warnings
from importlib import metadata
from typing import TYPE_CHECKING, Any, Optional

from promptmanager.script.base._api.deprecation import surface_promptmanager_deprecation_warnings

if TYPE_CHECKING:
    from promptmanager.script.base.schema import BaseCache


try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

verbose: bool = False
debug: bool = False
llm_cache: Optional["BaseCache"] = None


def _is_interactive_env() -> bool:
    """Determine if running within IPython or Jupyter."""
    import sys

    return hasattr(sys, "ps2")


def _warn_on_import(name: str) -> None:
    """Warn on import of deprecated module."""
    if _is_interactive_env():
        # No warnings for interactive environments.
        # This is done to avoid polluting the output of interactive environments
        # where users rely on auto-complete and may trigger this warning
        # even if they are not using any deprecated modules
        return
    warnings.warn(
        f"Importing {name} from promptmanager root module is no longer supported."
    )


# Surfaces Deprecation and Pending Deprecation warnings from promptmanager.script.base.
surface_promptmanager_deprecation_warnings()


def __getattr__(name: str) -> Any:
    if name == "MRKLChain":
        from promptmanager.script.base.agents import MRKLChain

        _warn_on_import(name)

        return MRKLChain
    elif name == "ReActChain":
        from promptmanager.script.base.agents import ReActChain

        _warn_on_import(name)

        return ReActChain
    elif name == "SelfAskWithSearchChain":
        from promptmanager.script.base.agents import SelfAskWithSearchChain

        _warn_on_import(name)

        return SelfAskWithSearchChain
    elif name == "ConversationChain":
        from promptmanager.script.base.chains import ConversationChain

        _warn_on_import(name)

        return ConversationChain
    elif name == "LLMBashChain":
        from promptmanager.script.base.chains import LLMBashChain

        _warn_on_import(name)

        return LLMBashChain
    elif name == "LLMChain":
        from promptmanager.script.base.chains import LLMChain

        _warn_on_import(name)

        return LLMChain
    elif name == "LLMCheckerChain":
        from promptmanager.script.base.chains import LLMCheckerChain

        _warn_on_import(name)

        return LLMCheckerChain
    elif name == "LLMMathChain":
        from promptmanager.script.base.chains import LLMMathChain

        _warn_on_import(name)

        return LLMMathChain
    elif name == "QAWithSourcesChain":
        from promptmanager.script.base.chains import QAWithSourcesChain

        _warn_on_import(name)

        return QAWithSourcesChain
    elif name == "VectorDBQA":
        from promptmanager.script.base.chains import VectorDBQA

        _warn_on_import(name)

        return VectorDBQA
    elif name == "VectorDBQAWithSourcesChain":
        from promptmanager.script.base.chains import VectorDBQAWithSourcesChain

        _warn_on_import(name)

        return VectorDBQAWithSourcesChain
    elif name == "InMemoryDocstore":
        from promptmanager.script.base.docstore import InMemoryDocstore

        _warn_on_import(name)

        return InMemoryDocstore
    elif name == "Wikipedia":
        from promptmanager.script.base.docstore import Wikipedia

        _warn_on_import(name)

        return Wikipedia
    elif name == "Anthropic":
        from promptmanager.script.base.llms import Anthropic

        _warn_on_import(name)

        return Anthropic
    elif name == "Banana":
        from promptmanager.script.base.llms import Banana

        _warn_on_import(name)

        return Banana
    elif name == "CerebriumAI":
        from promptmanager.script.base.llms import CerebriumAI

        _warn_on_import(name)

        return CerebriumAI
    elif name == "Cohere":
        from promptmanager.script.base.llms import Cohere

        _warn_on_import(name)

        return Cohere
    elif name == "ForefrontAI":
        from promptmanager.script.base.llms import ForefrontAI

        _warn_on_import(name)

        return ForefrontAI
    elif name == "GooseAI":
        from promptmanager.script.base.llms import GooseAI

        _warn_on_import(name)

        return GooseAI
    elif name == "HuggingFaceHub":
        from promptmanager.script.base.llms import HuggingFaceHub

        _warn_on_import(name)

        return HuggingFaceHub
    elif name == "HuggingFaceTextGenInference":
        from promptmanager.script.base.llms import HuggingFaceTextGenInference

        _warn_on_import(name)

        return HuggingFaceTextGenInference
    elif name == "LlamaCpp":
        from promptmanager.script.base.llms import LlamaCpp

        _warn_on_import(name)

        return LlamaCpp
    elif name == "Modal":
        from promptmanager.script.base.llms import Modal

        _warn_on_import(name)

        return Modal
    elif name == "OpenAI":
        from promptmanager.script.base.llms import OpenAI

        _warn_on_import(name)

        return OpenAI
    elif name == "Petals":
        from promptmanager.script.base.llms import Petals

        _warn_on_import(name)

        return Petals
    elif name == "PipelineAI":
        from promptmanager.script.base.llms import PipelineAI

        _warn_on_import(name)

        return PipelineAI
    elif name == "SagemakerEndpoint":
        from promptmanager.script.base.llms import SagemakerEndpoint

        _warn_on_import(name)

        return SagemakerEndpoint
    elif name == "StochasticAI":
        from promptmanager.script.base.llms import StochasticAI

        _warn_on_import(name)

        return StochasticAI
    elif name == "Writer":
        from promptmanager.script.base.llms import Writer

        _warn_on_import(name)

        return Writer
    elif name == "HuggingFacePipeline":
        from promptmanager.script.base.llms.huggingface_pipeline import HuggingFacePipeline

        _warn_on_import(name)

        return HuggingFacePipeline
    elif name == "FewShotPromptTemplate":
        from promptmanager.script.base.prompts import FewShotPromptTemplate

        _warn_on_import(name)

        return FewShotPromptTemplate
    elif name == "Prompt":
        from promptmanager.script.base.prompts import Prompt

        _warn_on_import(name)

        return Prompt
    elif name == "PromptTemplate":
        from promptmanager.script.base.prompts import PromptTemplate

        _warn_on_import(name)

        return PromptTemplate
    elif name == "BasePromptTemplate":
        from promptmanager.script.base.schema.prompt_template import BasePromptTemplate

        _warn_on_import(name)

        return BasePromptTemplate
    elif name == "ArxivAPIWrapper":
        from promptmanager.script.base.utilities import ArxivAPIWrapper

        _warn_on_import(name)

        return ArxivAPIWrapper
    elif name == "GoldenQueryAPIWrapper":
        from promptmanager.script.base.utilities import GoldenQueryAPIWrapper

        _warn_on_import(name)

        return GoldenQueryAPIWrapper
    elif name == "GoogleSearchAPIWrapper":
        from promptmanager.script.base.utilities import GoogleSearchAPIWrapper

        _warn_on_import(name)

        return GoogleSearchAPIWrapper
    elif name == "GoogleSerperAPIWrapper":
        from promptmanager.script.base.utilities import GoogleSerperAPIWrapper

        _warn_on_import(name)

        return GoogleSerperAPIWrapper
    elif name == "PowerBIDataset":
        from promptmanager.script.base.utilities import PowerBIDataset

        _warn_on_import(name)

        return PowerBIDataset
    elif name == "SearxSearchWrapper":
        from promptmanager.script.base.utilities import SearxSearchWrapper

        _warn_on_import(name)

        return SearxSearchWrapper
    elif name == "WikipediaAPIWrapper":
        from promptmanager.script.base.utilities import WikipediaAPIWrapper

        _warn_on_import(name)

        return WikipediaAPIWrapper
    elif name == "WolframAlphaAPIWrapper":
        from promptmanager.script.base.utilities import WolframAlphaAPIWrapper

        _warn_on_import(name)

        return WolframAlphaAPIWrapper
    elif name == "SQLDatabase":
        from promptmanager.script.base.utilities import SQLDatabase

        _warn_on_import(name)

        return SQLDatabase
    elif name == "FAISS":
        from promptmanager.script.base.vectorstores import FAISS

        _warn_on_import(name)

        return FAISS
    elif name == "ElasticVectorSearch":
        from promptmanager.script.base.vectorstores import ElasticVectorSearch

        _warn_on_import(name)

        return ElasticVectorSearch
    # For backwards compatibility
    elif name == "SerpAPIChain" or name == "SerpAPIWrapper":
        from promptmanager.script.base.utilities import SerpAPIWrapper

        _warn_on_import(name)

        return SerpAPIWrapper
    else:
        raise AttributeError(f"Could not find: {name}")


__all__ = [
    "LLMChain",
    "LLMBashChain",
    "LLMCheckerChain",
    "LLMMathChain",
    "ArxivAPIWrapper",
    "GoldenQueryAPIWrapper",
    "SelfAskWithSearchChain",
    "SerpAPIWrapper",
    "SerpAPIChain",
    "SearxSearchWrapper",
    "GoogleSearchAPIWrapper",
    "GoogleSerperAPIWrapper",
    "WolframAlphaAPIWrapper",
    "WikipediaAPIWrapper",
    "Anthropic",
    "Banana",
    "CerebriumAI",
    "Cohere",
    "ForefrontAI",
    "GooseAI",
    "Modal",
    "OpenAI",
    "Petals",
    "PipelineAI",
    "StochasticAI",
    "Writer",
    "BasePromptTemplate",
    "Prompt",
    "FewShotPromptTemplate",
    "PromptTemplate",
    "ReActChain",
    "Wikipedia",
    "HuggingFaceHub",
    "SagemakerEndpoint",
    "HuggingFacePipeline",
    "SQLDatabase",
    "PowerBIDataset",
    "FAISS",
    "MRKLChain",
    "VectorDBQA",
    "ElasticVectorSearch",
    "InMemoryDocstore",
    "ConversationChain",
    "VectorDBQAWithSourcesChain",
    "QAWithSourcesChain",
    "LlamaCpp",
    "HuggingFaceTextGenInference",
]
