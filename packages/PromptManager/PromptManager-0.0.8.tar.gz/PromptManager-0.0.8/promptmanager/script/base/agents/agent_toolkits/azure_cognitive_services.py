from __future__ import annotations

import sys
from typing import List

from promptmanager.script.base.agents.agent_toolkits.base import BaseToolkit
from promptmanager.script.base.tools.azure_cognitive_services import (
    AzureCogsFormRecognizerTool,
    AzureCogsImageAnalysisTool,
    AzureCogsSpeech2TextTool,
    AzureCogsText2SpeechTool,
)
from promptmanager.script.base.tools.base import BaseTool


class AzureCognitiveServicesToolkit(BaseToolkit):
    """Toolkit for Azure Cognitive Services."""

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""

        tools: List[BaseTool] = [
            AzureCogsFormRecognizerTool(),
            AzureCogsSpeech2TextTool(),
            AzureCogsText2SpeechTool(),
        ]

        # TODO: Remove check once azure-ai-vision supports MacOS.
        if sys.platform.startswith("linux") or sys.platform.startswith("win"):
            tools.append(AzureCogsImageAnalysisTool())
        return tools
