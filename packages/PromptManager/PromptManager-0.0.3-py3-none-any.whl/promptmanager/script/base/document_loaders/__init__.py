"""**Document Loaders**  are classes to load Documents.

**Document Loaders** are usually used to load a lot of Documents in a single run.

**Class hierarchy:**

.. code-block::

    BaseLoader --> <name>Loader  # Examples: TextLoader, UnstructuredFileLoader

**Main helpers:**

.. code-block::

    Document, <name>TextSplitter
"""

from promptmanager.script.base.document_loaders.acreom import AcreomLoader
from promptmanager.script.base.document_loaders.airbyte import (
    AirbyteCDKLoader,
    AirbyteGongLoader,
    AirbyteHubspotLoader,
    AirbyteSalesforceLoader,
    AirbyteShopifyLoader,
    AirbyteStripeLoader,
    AirbyteTypeformLoader,
    AirbyteZendeskSupportLoader,
)
from promptmanager.script.base.document_loaders.airbyte_json import AirbyteJSONLoader
from promptmanager.script.base.document_loaders.airtable import AirtableLoader
from promptmanager.script.base.document_loaders.apify_dataset import ApifyDatasetLoader
from promptmanager.script.base.document_loaders.arcgis_loader import ArcGISLoader
from promptmanager.script.base.document_loaders.arxiv import ArxivLoader
from promptmanager.script.base.document_loaders.assemblyai import AssemblyAIAudioTranscriptLoader
from promptmanager.script.base.document_loaders.async_html import AsyncHtmlLoader
from promptmanager.script.base.document_loaders.azlyrics import AZLyricsLoader
from promptmanager.script.base.document_loaders.azure_blob_storage_container import (
    AzureBlobStorageContainerLoader,
)
from promptmanager.script.base.document_loaders.azure_blob_storage_file import (
    AzureBlobStorageFileLoader,
)
from promptmanager.script.base.document_loaders.bibtex import BibtexLoader
from promptmanager.script.base.document_loaders.bigquery import BigQueryLoader
from promptmanager.script.base.document_loaders.bilibili import BiliBiliLoader
from promptmanager.script.base.document_loaders.blackboard import BlackboardLoader
from promptmanager.script.base.document_loaders.blob_loaders import (
    Blob,
    BlobLoader,
    FileSystemBlobLoader,
    YoutubeAudioLoader,
)
from promptmanager.script.base.document_loaders.blockchain import BlockchainDocumentLoader
from promptmanager.script.base.document_loaders.brave_search import BraveSearchLoader
from promptmanager.script.base.document_loaders.browserless import BrowserlessLoader
from promptmanager.script.base.document_loaders.chatgpt import ChatGPTLoader
from promptmanager.script.base.document_loaders.chromium import AsyncChromiumLoader
from promptmanager.script.base.document_loaders.college_confidential import CollegeConfidentialLoader
from promptmanager.script.base.document_loaders.concurrent import ConcurrentLoader
from promptmanager.script.base.document_loaders.confluence import ConfluenceLoader
from promptmanager.script.base.document_loaders.conllu import CoNLLULoader
from promptmanager.script.base.document_loaders.csv_loader import CSVLoader, UnstructuredCSVLoader
from promptmanager.script.base.document_loaders.cube_semantic import CubeSemanticLoader
from promptmanager.script.base.document_loaders.datadog_logs import DatadogLogsLoader
from promptmanager.script.base.document_loaders.dataframe import DataFrameLoader
from promptmanager.script.base.document_loaders.diffbot import DiffbotLoader
from promptmanager.script.base.document_loaders.directory import DirectoryLoader
from promptmanager.script.base.document_loaders.discord import DiscordChatLoader
from promptmanager.script.base.document_loaders.docugami import DocugamiLoader
from promptmanager.script.base.document_loaders.dropbox import DropboxLoader
from promptmanager.script.base.document_loaders.duckdb_loader import DuckDBLoader
from promptmanager.script.base.document_loaders.email import (
    OutlookMessageLoader,
    UnstructuredEmailLoader,
)
from promptmanager.script.base.document_loaders.embaas import EmbaasBlobLoader, EmbaasLoader
from promptmanager.script.base.document_loaders.epub import UnstructuredEPubLoader
from promptmanager.script.base.document_loaders.etherscan import EtherscanLoader
from promptmanager.script.base.document_loaders.evernote import EverNoteLoader
from promptmanager.script.base.document_loaders.excel import UnstructuredExcelLoader
from promptmanager.script.base.document_loaders.facebook_chat import FacebookChatLoader
from promptmanager.script.base.document_loaders.fauna import FaunaLoader
from promptmanager.script.base.document_loaders.figma import FigmaFileLoader
from promptmanager.script.base.document_loaders.gcs_directory import GCSDirectoryLoader
from promptmanager.script.base.document_loaders.gcs_file import GCSFileLoader
from promptmanager.script.base.document_loaders.geodataframe import GeoDataFrameLoader
from promptmanager.script.base.document_loaders.git import GitLoader
from promptmanager.script.base.document_loaders.gitbook import GitbookLoader
from promptmanager.script.base.document_loaders.github import GitHubIssuesLoader
from promptmanager.script.base.document_loaders.googledrive import GoogleDriveLoader
from promptmanager.script.base.document_loaders.gutenberg import GutenbergLoader
from promptmanager.script.base.document_loaders.hn import HNLoader
from promptmanager.script.base.document_loaders.html import UnstructuredHTMLLoader
from promptmanager.script.base.document_loaders.html_bs import BSHTMLLoader
from promptmanager.script.base.document_loaders.hugging_face_dataset import HuggingFaceDatasetLoader
from promptmanager.script.base.document_loaders.ifixit import IFixitLoader
from promptmanager.script.base.document_loaders.image import UnstructuredImageLoader
from promptmanager.script.base.document_loaders.image_captions import ImageCaptionLoader
from promptmanager.script.base.document_loaders.imsdb import IMSDbLoader
from promptmanager.script.base.document_loaders.iugu import IuguLoader
from promptmanager.script.base.document_loaders.joplin import JoplinLoader
from promptmanager.script.base.document_loaders.json_loader import JSONLoader
from promptmanager.script.base.document_loaders.larksuite import LarkSuiteDocLoader
from promptmanager.script.base.document_loaders.markdown import UnstructuredMarkdownLoader
from promptmanager.script.base.document_loaders.mastodon import MastodonTootsLoader
from promptmanager.script.base.document_loaders.max_compute import MaxComputeLoader
from promptmanager.script.base.document_loaders.mediawikidump import MWDumpLoader
from promptmanager.script.base.document_loaders.merge import MergedDataLoader
from promptmanager.script.base.document_loaders.mhtml import MHTMLLoader
from promptmanager.script.base.document_loaders.modern_treasury import ModernTreasuryLoader
from promptmanager.script.base.document_loaders.mongodb import MongodbLoader
from promptmanager.script.base.document_loaders.news import NewsURLLoader
from promptmanager.script.base.document_loaders.notebook import NotebookLoader
from promptmanager.script.base.document_loaders.notion import NotionDirectoryLoader
from promptmanager.script.base.document_loaders.notiondb import NotionDBLoader
from promptmanager.script.base.document_loaders.obs_directory import OBSDirectoryLoader
from promptmanager.script.base.document_loaders.obs_file import OBSFileLoader
from promptmanager.script.base.document_loaders.obsidian import ObsidianLoader
from promptmanager.script.base.document_loaders.odt import UnstructuredODTLoader
from promptmanager.script.base.document_loaders.onedrive import OneDriveLoader
from promptmanager.script.base.document_loaders.onedrive_file import OneDriveFileLoader
from promptmanager.script.base.document_loaders.open_city_data import OpenCityDataLoader
from promptmanager.script.base.document_loaders.org_mode import UnstructuredOrgModeLoader
from promptmanager.script.base.document_loaders.pdf import (
    AmazonTextractPDFLoader,
    MathpixPDFLoader,
    OnlinePDFLoader,
    PDFMinerLoader,
    PDFMinerPDFasHTMLLoader,
    PDFPlumberLoader,
    PyMuPDFLoader,
    PyPDFDirectoryLoader,
    PyPDFium2Loader,
    PyPDFLoader,
    UnstructuredPDFLoader,
)
from promptmanager.script.base.document_loaders.polars_dataframe import PolarsDataFrameLoader
from promptmanager.script.base.document_loaders.powerpoint import UnstructuredPowerPointLoader
from promptmanager.script.base.document_loaders.psychic import PsychicLoader
from promptmanager.script.base.document_loaders.pubmed import PubMedLoader
from promptmanager.script.base.document_loaders.pyspark_dataframe import PySparkDataFrameLoader
from promptmanager.script.base.document_loaders.python import PythonLoader
from promptmanager.script.base.document_loaders.readthedocs import ReadTheDocsLoader
from promptmanager.script.base.document_loaders.recursive_url_loader import RecursiveUrlLoader
from promptmanager.script.base.document_loaders.reddit import RedditPostsLoader
from promptmanager.script.base.document_loaders.roam import RoamLoader
from promptmanager.script.base.document_loaders.rocksetdb import RocksetLoader
from promptmanager.script.base.document_loaders.rss import RSSFeedLoader
from promptmanager.script.base.document_loaders.rst import UnstructuredRSTLoader
from promptmanager.script.base.document_loaders.rtf import UnstructuredRTFLoader
from promptmanager.script.base.document_loaders.s3_directory import S3DirectoryLoader
from promptmanager.script.base.document_loaders.s3_file import S3FileLoader
from promptmanager.script.base.document_loaders.sharepoint import SharePointLoader
from promptmanager.script.base.document_loaders.sitemap import SitemapLoader
from promptmanager.script.base.document_loaders.slack_directory import SlackDirectoryLoader
from promptmanager.script.base.document_loaders.snowflake_loader import SnowflakeLoader
from promptmanager.script.base.document_loaders.spreedly import SpreedlyLoader
from promptmanager.script.base.document_loaders.srt import SRTLoader
from promptmanager.script.base.document_loaders.stripe import StripeLoader
from promptmanager.script.base.document_loaders.telegram import (
    TelegramChatApiLoader,
    TelegramChatFileLoader,
)
from promptmanager.script.base.document_loaders.tencent_cos_directory import TencentCOSDirectoryLoader
from promptmanager.script.base.document_loaders.tencent_cos_file import TencentCOSFileLoader
from promptmanager.script.base.document_loaders.tensorflow_datasets import TensorflowDatasetLoader
from promptmanager.script.base.document_loaders.text import TextLoader
from promptmanager.script.base.document_loaders.tomarkdown import ToMarkdownLoader
from promptmanager.script.base.document_loaders.toml import TomlLoader
from promptmanager.script.base.document_loaders.trello import TrelloLoader
from promptmanager.script.base.document_loaders.tsv import UnstructuredTSVLoader
from promptmanager.script.base.document_loaders.twitter import TwitterTweetLoader
from promptmanager.script.base.document_loaders.unstructured import (
    UnstructuredAPIFileIOLoader,
    UnstructuredAPIFileLoader,
    UnstructuredFileIOLoader,
    UnstructuredFileLoader,
)
from promptmanager.script.base.document_loaders.url import UnstructuredURLLoader
from promptmanager.script.base.document_loaders.url_playwright import PlaywrightURLLoader
from promptmanager.script.base.document_loaders.url_selenium import SeleniumURLLoader
from promptmanager.script.base.document_loaders.weather import WeatherDataLoader
from promptmanager.script.base.document_loaders.web_base import WebBaseLoader
from promptmanager.script.base.document_loaders.whatsapp_chat import WhatsAppChatLoader
from promptmanager.script.base.document_loaders.wikipedia import WikipediaLoader
from promptmanager.script.base.document_loaders.word_document import (
    Docx2txtLoader,
    UnstructuredWordDocumentLoader,
)
from promptmanager.script.base.document_loaders.xml import UnstructuredXMLLoader
from promptmanager.script.base.document_loaders.xorbits import XorbitsLoader
from promptmanager.script.base.document_loaders.youtube import (
    GoogleApiClient,
    GoogleApiYoutubeLoader,
    YoutubeLoader,
)

# Legacy: only for backwards compatibility. Use PyPDFLoader instead
PagedPDFSplitter = PyPDFLoader

# For backwards compatibility
TelegramChatLoader = TelegramChatFileLoader

__all__ = [
    "AcreomLoader",
    "AsyncHtmlLoader",
    "AsyncChromiumLoader",
    "AZLyricsLoader",
    "AcreomLoader",
    "AirbyteCDKLoader",
    "AirbyteGongLoader",
    "AirbyteJSONLoader",
    "AirbyteHubspotLoader",
    "AirbyteSalesforceLoader",
    "AirbyteShopifyLoader",
    "AirbyteStripeLoader",
    "AirbyteTypeformLoader",
    "AirbyteZendeskSupportLoader",
    "AirtableLoader",
    "AmazonTextractPDFLoader",
    "ApifyDatasetLoader",
    "ArcGISLoader",
    "ArxivLoader",
    "AssemblyAIAudioTranscriptLoader",
    "AsyncHtmlLoader",
    "AzureBlobStorageContainerLoader",
    "AzureBlobStorageFileLoader",
    "BSHTMLLoader",
    "BibtexLoader",
    "BigQueryLoader",
    "BiliBiliLoader",
    "BlackboardLoader",
    "Blob",
    "BlobLoader",
    "BlockchainDocumentLoader",
    "BraveSearchLoader",
    "BrowserlessLoader",
    "CSVLoader",
    "ChatGPTLoader",
    "CoNLLULoader",
    "CollegeConfidentialLoader",
    "ConcurrentLoader",
    "ConfluenceLoader",
    "CubeSemanticLoader",
    "DataFrameLoader",
    "DatadogLogsLoader",
    "DiffbotLoader",
    "DirectoryLoader",
    "DiscordChatLoader",
    "DocugamiLoader",
    "Docx2txtLoader",
    "DropboxLoader",
    "DuckDBLoader",
    "EmbaasBlobLoader",
    "EmbaasLoader",
    "EtherscanLoader",
    "EverNoteLoader",
    "FacebookChatLoader",
    "FaunaLoader",
    "FigmaFileLoader",
    "FileSystemBlobLoader",
    "GCSDirectoryLoader",
    "GCSFileLoader",
    "GeoDataFrameLoader",
    "GitHubIssuesLoader",
    "GitLoader",
    "GitbookLoader",
    "GoogleApiClient",
    "GoogleApiYoutubeLoader",
    "GoogleDriveLoader",
    "GutenbergLoader",
    "HNLoader",
    "HuggingFaceDatasetLoader",
    "IFixitLoader",
    "IMSDbLoader",
    "ImageCaptionLoader",
    "IuguLoader",
    "JSONLoader",
    "JoplinLoader",
    "LarkSuiteDocLoader",
    "MHTMLLoader",
    "MWDumpLoader",
    "MastodonTootsLoader",
    "MathpixPDFLoader",
    "MaxComputeLoader",
    "MergedDataLoader",
    "ModernTreasuryLoader",
    "MongodbLoader",
    "NewsURLLoader",
    "NotebookLoader",
    "NotionDBLoader",
    "NotionDirectoryLoader",
    "OBSDirectoryLoader",
    "OBSFileLoader",
    "ObsidianLoader",
    "OneDriveFileLoader",
    "OneDriveLoader",
    "OnlinePDFLoader",
    "OpenCityDataLoader",
    "OutlookMessageLoader",
    "PDFMinerLoader",
    "PDFMinerPDFasHTMLLoader",
    "PDFPlumberLoader",
    "PagedPDFSplitter",
    "PlaywrightURLLoader",
    "PolarsDataFrameLoader",
    "PsychicLoader",
    "PubMedLoader",
    "PyMuPDFLoader",
    "PyPDFDirectoryLoader",
    "PyPDFLoader",
    "PyPDFium2Loader",
    "PySparkDataFrameLoader",
    "PythonLoader",
    "RSSFeedLoader",
    "ReadTheDocsLoader",
    "RecursiveUrlLoader",
    "RedditPostsLoader",
    "RoamLoader",
    "RocksetLoader",
    "S3DirectoryLoader",
    "S3FileLoader",
    "SRTLoader",
    "SeleniumURLLoader",
    "SharePointLoader",
    "SitemapLoader",
    "SlackDirectoryLoader",
    "SnowflakeLoader",
    "SpreedlyLoader",
    "StripeLoader",
    "TelegramChatApiLoader",
    "TelegramChatFileLoader",
    "TelegramChatLoader",
    "TensorflowDatasetLoader",
    "TencentCOSDirectoryLoader",
    "TencentCOSFileLoader",
    "TextLoader",
    "ToMarkdownLoader",
    "TomlLoader",
    "TrelloLoader",
    "TwitterTweetLoader",
    "UnstructuredAPIFileIOLoader",
    "UnstructuredAPIFileLoader",
    "UnstructuredCSVLoader",
    "UnstructuredEPubLoader",
    "UnstructuredEmailLoader",
    "UnstructuredExcelLoader",
    "UnstructuredFileIOLoader",
    "UnstructuredFileLoader",
    "UnstructuredHTMLLoader",
    "UnstructuredImageLoader",
    "UnstructuredMarkdownLoader",
    "UnstructuredODTLoader",
    "UnstructuredOrgModeLoader",
    "UnstructuredPDFLoader",
    "UnstructuredPowerPointLoader",
    "UnstructuredRSTLoader",
    "UnstructuredRTFLoader",
    "UnstructuredTSVLoader",
    "UnstructuredURLLoader",
    "UnstructuredWordDocumentLoader",
    "UnstructuredXMLLoader",
    "WeatherDataLoader",
    "WebBaseLoader",
    "WhatsAppChatLoader",
    "WikipediaLoader",
    "XorbitsLoader",
    "YoutubeAudioLoader",
    "YoutubeLoader",
]
