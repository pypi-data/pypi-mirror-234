"""**Schemas** are the Promptmanager Base Classes and Interfaces."""
from promptmanager.script.base.schema.agent import AgentAction, AgentFinish
from promptmanager.script.base.schema.cache import BaseCache
from promptmanager.script.base.schema.chat_history import BaseChatMessageHistory
from promptmanager.script.base.schema.document import BaseDocumentTransformer, Document
from promptmanager.script.base.schema.exceptions import PMException
from promptmanager.script.base.schema.memory import BaseMemory
from promptmanager.script.base.schema.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
    _message_from_dict,
    _message_to_dict,
    get_buffer_string,
    messages_from_dict,
    messages_to_dict,
)
from promptmanager.script.base.schema.output import (
    ChatGeneration,
    ChatResult,
    Generation,
    LLMResult,
    RunInfo,
)
from promptmanager.script.base.schema.output_parser import (
    BaseLLMOutputParser,
    BaseOutputParser,
    OutputParserException,
    StrOutputParser,
)
from promptmanager.script.base.schema.prompt import PromptValue
from promptmanager.script.base.schema.prompt_template import BasePromptTemplate, format_document
from promptmanager.script.base.schema.retriever import BaseRetriever
from promptmanager.script.base.schema.storage import BaseStore

RUN_KEY = "__run"
Memory = BaseMemory

__all__ = [
    "BaseCache",
    "BaseMemory",
    "BaseStore",
    "AgentFinish",
    "AgentAction",
    "Document",
    "BaseChatMessageHistory",
    "BaseDocumentTransformer",
    "BaseMessage",
    "ChatMessage",
    "FunctionMessage",
    "HumanMessage",
    "AIMessage",
    "SystemMessage",
    "messages_from_dict",
    "messages_to_dict",
    "_message_to_dict",
    "_message_from_dict",
    "get_buffer_string",
    "RunInfo",
    "LLMResult",
    "ChatResult",
    "ChatGeneration",
    "Generation",
    "PromptValue",
    "PMException",
    "BaseRetriever",
    "RUN_KEY",
    "Memory",
    "OutputParserException",
    "StrOutputParser",
    "BaseOutputParser",
    "BaseLLMOutputParser",
    "BasePromptTemplate",
    "format_document",
]
