"""
**Agent** is a class that uses an LLM to choose a sequence of actions to take.

In Chains, a sequence of actions is hardcoded. In Agents,
a language model is used as a reasoning engine to determine which actions
to take and in which order.

Agents select and use **Tools** and **Toolkits** for actions.

**Class hierarchy:**

.. code-block::

    BaseSingleActionAgent --> LLMSingleActionAgent
                              OpenAIFunctionsAgent
                              XMLAgent
                              Agent --> <name>Agent  # Examples: ZeroShotAgent, ChatAgent
                                        

    BaseMultiActionAgent  --> OpenAIMultiFunctionsAgent
    
    
**Main helpers:**

.. code-block::

    AgentType, AgentExecutor, AgentOutputParser, AgentExecutorIterator,
    AgentAction, AgentFinish
    
"""  # noqa: E501
from promptmanager.script.base.agents.agent import (
    Agent,
    AgentExecutor,
    AgentOutputParser,
    BaseMultiActionAgent,
    BaseSingleActionAgent,
    LLMSingleActionAgent,
)
from promptmanager.script.base.agents.agent_iterator import AgentExecutorIterator
from promptmanager.script.base.agents.agent_toolkits import (
    create_csv_agent,
    create_json_agent,
    create_openapi_agent,
    create_pandas_dataframe_agent,
    create_pbi_agent,
    create_pbi_chat_agent,
    create_spark_dataframe_agent,
    create_spark_sql_agent,
    create_sql_agent,
    create_vectorstore_agent,
    create_vectorstore_router_agent,
    create_xorbits_agent,
)
from promptmanager.script.base.agents.agent_types import AgentType
from promptmanager.script.base.agents.conversational.base import ConversationalAgent
from promptmanager.script.base.agents.conversational_chat.base import ConversationalChatAgent
from promptmanager.script.base.agents.initialize import initialize_agent
from promptmanager.script.base.agents.load_tools import (
    get_all_tool_names,
    load_huggingface_tool,
    load_tools,
)
from promptmanager.script.base.agents.loading import load_agent
from promptmanager.script.base.agents.mrkl.base import MRKLChain, ZeroShotAgent
from promptmanager.script.base.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from promptmanager.script.base.agents.openai_functions_multi_agent.base import OpenAIMultiFunctionsAgent
from promptmanager.script.base.agents.react.base import ReActChain, ReActTextWorldAgent
from promptmanager.script.base.agents.self_ask_with_search.base import SelfAskWithSearchChain
from promptmanager.script.base.agents.structured_chat.base import StructuredChatAgent
from promptmanager.script.base.agents.tools import Tool, tool
from promptmanager.script.base.agents.xml.base import XMLAgent

__all__ = [
    "Agent",
    "AgentExecutor",
    "AgentExecutorIterator",
    "AgentOutputParser",
    "AgentType",
    "BaseMultiActionAgent",
    "BaseSingleActionAgent",
    "ConversationalAgent",
    "ConversationalChatAgent",
    "LLMSingleActionAgent",
    "MRKLChain",
    "OpenAIFunctionsAgent",
    "OpenAIMultiFunctionsAgent",
    "ReActChain",
    "ReActTextWorldAgent",
    "SelfAskWithSearchChain",
    "StructuredChatAgent",
    "Tool",
    "ZeroShotAgent",
    "create_csv_agent",
    "create_json_agent",
    "create_openapi_agent",
    "create_pandas_dataframe_agent",
    "create_pbi_agent",
    "create_pbi_chat_agent",
    "create_spark_dataframe_agent",
    "create_spark_sql_agent",
    "create_sql_agent",
    "create_vectorstore_agent",
    "create_vectorstore_router_agent",
    "get_all_tool_names",
    "initialize_agent",
    "load_agent",
    "load_huggingface_tool",
    "load_tools",
    "tool",
    "create_xorbits_agent",
    "XMLAgent",
]
