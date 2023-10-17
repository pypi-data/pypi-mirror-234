"""Azure Cognitive Services Tools."""

from promptmanager.script.base.tools.azure_cognitive_services.form_recognizer import (
    AzureCogsFormRecognizerTool,
)
from promptmanager.script.base.tools.azure_cognitive_services.image_analysis import (
    AzureCogsImageAnalysisTool,
)
from promptmanager.script.base.tools.azure_cognitive_services.speech2text import (
    AzureCogsSpeech2TextTool,
)
from promptmanager.script.base.tools.azure_cognitive_services.text2speech import (
    AzureCogsText2SpeechTool,
)

__all__ = [
    "AzureCogsImageAnalysisTool",
    "AzureCogsFormRecognizerTool",
    "AzureCogsSpeech2TextTool",
    "AzureCogsText2SpeechTool",
]
