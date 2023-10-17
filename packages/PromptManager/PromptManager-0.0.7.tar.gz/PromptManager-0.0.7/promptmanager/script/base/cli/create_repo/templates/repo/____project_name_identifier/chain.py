"""This is a template for a custom chain.

Edit this file to implement your chain logic.
"""

from typing import Optional

from promptmanager.script.base.chat_models.openai import ChatOpenAI
from promptmanager.script.base.output_parsers.list import CommaSeparatedListOutputParser
from promptmanager.script.base.prompts.chat import ChatPromptTemplate
from promptmanager.script.base.schema.language_model import BaseLanguageModel
from promptmanager.script.base.schema.runnable import Runnable

template = """You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
ONLY return a comma separated list, and nothing more."""  # noqa: E501
human_template = "{text}"


def get_chain(model: Optional[BaseLanguageModel] = None) -> Runnable:
    """Return a chain."""
    model = model or ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("human", human_template),
        ]
    )
    return prompt | model | CommaSeparatedListOutputParser()
