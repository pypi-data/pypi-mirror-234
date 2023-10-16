"""**Prompt** is the input to the model.

Prompt is often constructed
from multiple components. Prompt classes and functions make constructing
 and working with prompts easy.

**Class hierarchy:**

.. code-block::

    BasePromptTemplate --> PipelinePromptTemplate
                           StringPromptTemplate --> PromptTemplate
                                                    FewShotPromptTemplate
                                                    FewShotPromptWithTemplates
                           BaseChatPromptTemplate --> AutoGPTPrompt
                                                      ChatPromptTemplate --> AgentScratchPadChatPromptTemplate



    BaseMessagePromptTemplate --> MessagesPlaceholder
                                  BaseStringMessagePromptTemplate --> ChatMessagePromptTemplate
                                                                      HumanMessagePromptTemplate
                                                                      AIMessagePromptTemplate
                                                                      SystemMessagePromptTemplate

    PromptValue --> StringPromptValue
                    ChatPromptValue

"""  # noqa: E501
from promptmanager.script.base.prompts.base import StringPromptTemplate
from promptmanager.script.base.prompts.chat import (
    AIMessagePromptTemplate,
    BaseChatPromptTemplate,
    ChatMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from promptmanager.script.base.prompts.example_selector import (
    LengthBasedExampleSelector,
    MaxMarginalRelevanceExampleSelector,
    NGramOverlapExampleSelector,
    SemanticSimilarityExampleSelector,
)
from promptmanager.script.base.prompts.few_shot import (
    FewShotChatMessagePromptTemplate,
    FewShotPromptTemplate,
)
from promptmanager.script.base.prompts.few_shot_with_templates import FewShotPromptWithTemplates
from promptmanager.script.base.prompts.loading import load_prompt
from promptmanager.script.base.prompts.pipeline import PipelinePromptTemplate
from promptmanager.script.base.prompts.prompt import Prompt, PromptTemplate
from promptmanager.script.base.schema.prompt_template import BasePromptTemplate

__all__ = [
    "AIMessagePromptTemplate",
    "BaseChatPromptTemplate",
    "BasePromptTemplate",
    "ChatMessagePromptTemplate",
    "ChatPromptTemplate",
    "FewShotPromptTemplate",
    "FewShotPromptWithTemplates",
    "HumanMessagePromptTemplate",
    "LengthBasedExampleSelector",
    "MaxMarginalRelevanceExampleSelector",
    "MessagesPlaceholder",
    "NGramOverlapExampleSelector",
    "PipelinePromptTemplate",
    "Prompt",
    "PromptTemplate",
    "SemanticSimilarityExampleSelector",
    "StringPromptTemplate",
    "SystemMessagePromptTemplate",
    "load_prompt",
    "FewShotChatMessagePromptTemplate",
]
