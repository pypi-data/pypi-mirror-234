"""**Tools** are classes that an Agent uses to interact with the world.

Each tool has a **description**. Agent uses the description to choose the right
tool for the job.

**Class hierarchy:**

.. code-block::

    ToolMetaclass --> BaseTool --> <name>Tool  # Examples: AIPluginTool, BaseGraphQLTool
                                   <name>      # Examples: BraveSearch, HumanInputRun

**Main helpers:**

.. code-block::

    CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
"""

from promptmanager.script.base.tools.ainetwork.app import AINAppOps
from promptmanager.script.base.tools.ainetwork.owner import AINOwnerOps
from promptmanager.script.base.tools.ainetwork.rule import AINRuleOps
from promptmanager.script.base.tools.ainetwork.transfer import AINTransfer
from promptmanager.script.base.tools.ainetwork.value import AINValueOps
from promptmanager.script.base.tools.arxiv.tool import ArxivQueryRun
from promptmanager.script.base.tools.azure_cognitive_services import (
    AzureCogsFormRecognizerTool,
    AzureCogsImageAnalysisTool,
    AzureCogsSpeech2TextTool,
    AzureCogsText2SpeechTool,
)
from promptmanager.script.base.tools.base import BaseTool, StructuredTool, Tool, tool
from promptmanager.script.base.tools.bing_search.tool import BingSearchResults, BingSearchRun
from promptmanager.script.base.tools.brave_search.tool import BraveSearch
from promptmanager.script.base.tools.ddg_search.tool import DuckDuckGoSearchResults, DuckDuckGoSearchRun
from promptmanager.script.base.tools.edenai import (
    EdenAiExplicitImageTool,
    EdenAiObjectDetectionTool,
    EdenAiParsingIDTool,
    EdenAiParsingInvoiceTool,
    EdenAiSpeechToTextTool,
    EdenAiTextModerationTool,
    EdenAiTextToSpeechTool,
    EdenaiTool,
)
from promptmanager.script.base.tools.eleven_labs.text2speech import ElevenLabsText2SpeechTool
from promptmanager.script.base.tools.file_management import (
    CopyFileTool,
    DeleteFileTool,
    FileSearchTool,
    ListDirectoryTool,
    MoveFileTool,
    ReadFileTool,
    WriteFileTool,
)
from promptmanager.script.base.tools.gmail import (
    GmailCreateDraft,
    GmailGetMessage,
    GmailGetThread,
    GmailSearch,
    GmailSendMessage,
)
from promptmanager.script.base.tools.google_places.tool import GooglePlacesTool
from promptmanager.script.base.tools.google_search.tool import GoogleSearchResults, GoogleSearchRun
from promptmanager.script.base.tools.google_serper.tool import GoogleSerperResults, GoogleSerperRun
from promptmanager.script.base.tools.graphql.tool import BaseGraphQLTool
from promptmanager.script.base.tools.human.tool import HumanInputRun
from promptmanager.script.base.tools.ifttt import IFTTTWebhook
from promptmanager.script.base.tools.interaction.tool import StdInInquireTool
from promptmanager.script.base.tools.jira.tool import JiraAction
from promptmanager.script.base.tools.json.tool import JsonGetValueTool, JsonListKeysTool
from promptmanager.script.base.tools.metaphor_search import MetaphorSearchResults
from promptmanager.script.base.tools.office365.create_draft_message import O365CreateDraftMessage
from promptmanager.script.base.tools.office365.events_search import O365SearchEvents
from promptmanager.script.base.tools.office365.messages_search import O365SearchEmails
from promptmanager.script.base.tools.office365.send_event import O365SendEvent
from promptmanager.script.base.tools.office365.send_message import O365SendMessage
from promptmanager.script.base.tools.office365.utils import authenticate
from promptmanager.script.base.tools.openapi.utils.api_models import APIOperation
from promptmanager.script.base.tools.openapi.utils.openapi_utils import OpenAPISpec
from promptmanager.script.base.tools.openweathermap.tool import OpenWeatherMapQueryRun
from promptmanager.script.base.tools.playwright import (
    ClickTool,
    CurrentWebPageTool,
    ExtractHyperlinksTool,
    ExtractTextTool,
    GetElementsTool,
    NavigateBackTool,
    NavigateTool,
)
from promptmanager.script.base.tools.plugin import AIPluginTool
from promptmanager.script.base.tools.powerbi.tool import (
    InfoPowerBITool,
    ListPowerBITool,
    QueryPowerBITool,
)
from promptmanager.script.base.tools.pubmed.tool import PubmedQueryRun
from promptmanager.script.base.tools.python.tool import PythonAstREPLTool, PythonREPLTool
from promptmanager.script.base.tools.render import format_tool_to_openai_function
from promptmanager.script.base.tools.requests.tool import (
    BaseRequestsTool,
    RequestsDeleteTool,
    RequestsGetTool,
    RequestsPatchTool,
    RequestsPostTool,
    RequestsPutTool,
)
from promptmanager.script.base.tools.scenexplain.tool import SceneXplainTool
from promptmanager.script.base.tools.searx_search.tool import SearxSearchResults, SearxSearchRun
from promptmanager.script.base.tools.shell.tool import ShellTool
from promptmanager.script.base.tools.sleep.tool import SleepTool
from promptmanager.script.base.tools.spark_sql.tool import (
    BaseSparkSQLTool,
    InfoSparkSQLTool,
    ListSparkSQLTool,
    QueryCheckerTool,
    QuerySparkSQLTool,
)
from promptmanager.script.base.tools.sql_database.tool import (
    BaseSQLDatabaseTool,
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from promptmanager.script.base.tools.steamship_image_generation import SteamshipImageGenerationTool
from promptmanager.script.base.tools.vectorstore.tool import (
    VectorStoreQATool,
    VectorStoreQAWithSourcesTool,
)
from promptmanager.script.base.tools.wikipedia.tool import WikipediaQueryRun
from promptmanager.script.base.tools.wolfram_alpha.tool import WolframAlphaQueryRun
from promptmanager.script.base.tools.youtube.search import YouTubeSearchTool
from promptmanager.script.base.tools.zapier.tool import ZapierNLAListActions, ZapierNLARunAction

__all__ = [
    "AINAppOps",
    "AINOwnerOps",
    "AINRuleOps",
    "AINTransfer",
    "AINValueOps",
    "AIPluginTool",
    "APIOperation",
    "ArxivQueryRun",
    "AzureCogsFormRecognizerTool",
    "AzureCogsImageAnalysisTool",
    "AzureCogsSpeech2TextTool",
    "AzureCogsText2SpeechTool",
    "BaseGraphQLTool",
    "BaseRequestsTool",
    "BaseSQLDatabaseTool",
    "BaseSparkSQLTool",
    "BaseTool",
    "BingSearchResults",
    "BingSearchRun",
    "BraveSearch",
    "ClickTool",
    "CopyFileTool",
    "CurrentWebPageTool",
    "DeleteFileTool",
    "DuckDuckGoSearchResults",
    "DuckDuckGoSearchRun",
    "EdenAiExplicitImageTool",
    "EdenAiObjectDetectionTool",
    "EdenAiParsingIDTool",
    "EdenAiParsingInvoiceTool",
    "EdenAiTextToSpeechTool",
    "EdenAiSpeechToTextTool",
    "EdenAiTextModerationTool",
    "EdenaiTool",
    "ElevenLabsText2SpeechTool",
    "ExtractHyperlinksTool",
    "ExtractTextTool",
    "FileSearchTool",
    "GetElementsTool",
    "GmailCreateDraft",
    "GmailGetMessage",
    "GmailGetThread",
    "GmailSearch",
    "GmailSendMessage",
    "GooglePlacesTool",
    "GoogleSearchResults",
    "GoogleSearchRun",
    "GoogleSerperResults",
    "GoogleSerperRun",
    "HumanInputRun",
    "IFTTTWebhook",
    "InfoPowerBITool",
    "InfoSQLDatabaseTool",
    "InfoSparkSQLTool",
    "JiraAction",
    "JsonGetValueTool",
    "JsonListKeysTool",
    "ListDirectoryTool",
    "ListPowerBITool",
    "ListSQLDatabaseTool",
    "ListSparkSQLTool",
    "MetaphorSearchResults",
    "MoveFileTool",
    "NavigateBackTool",
    "NavigateTool",
    "O365SearchEmails",
    "O365SearchEvents",
    "O365CreateDraftMessage",
    "O365SendMessage",
    "O365SendEvent",
    "authenticate",
    "OpenAPISpec",
    "OpenWeatherMapQueryRun",
    "PubmedQueryRun",
    "PythonAstREPLTool",
    "PythonREPLTool",
    "QueryCheckerTool",
    "QueryPowerBITool",
    "QuerySQLCheckerTool",
    "QuerySQLDataBaseTool",
    "QuerySparkSQLTool",
    "ReadFileTool",
    "RequestsDeleteTool",
    "RequestsGetTool",
    "RequestsPatchTool",
    "RequestsPostTool",
    "RequestsPutTool",
    "SceneXplainTool",
    "SearxSearchResults",
    "SearxSearchRun",
    "ShellTool",
    "SleepTool",
    "StdInInquireTool",
    "SteamshipImageGenerationTool",
    "StructuredTool",
    "Tool",
    "VectorStoreQATool",
    "VectorStoreQAWithSourcesTool",
    "WikipediaQueryRun",
    "WolframAlphaQueryRun",
    "WriteFileTool",
    "YouTubeSearchTool",
    "ZapierNLAListActions",
    "ZapierNLARunAction",
    "tool",
    "format_tool_to_openai_function",
]
