"""LLM Chain for generating examples for question answering."""
from __future__ import annotations

from typing import Any

from promptmanager.script.base.chains.llm import LLMChain
from promptmanager.script.base.evaluation.qa.generate_prompt import PROMPT
from promptmanager.script.base.output_parsers.regex import RegexParser
from promptmanager.script.base.pydantic_v1 import Field
from promptmanager.script.base.schema.language_model import BaseLanguageModel
from promptmanager.script.base.schema.output_parser import BaseLLMOutputParser

_QA_OUTPUT_PARSER = RegexParser(
    regex=r"QUESTION: (.*?)\n+ANSWER: (.*)", output_keys=["query", "answer"]
)


class QAGenerateChain(LLMChain):
    """LLM Chain for generating examples for question answering."""

    output_parser: BaseLLMOutputParser = Field(default=_QA_OUTPUT_PARSER)
    output_key: str = "qa_pairs"

    @classmethod
    def from_llm(cls, llm: BaseLanguageModel, **kwargs: Any) -> QAGenerateChain:
        """Load QA Generate Chain from LLM."""
        return cls(llm=llm, prompt=PROMPT, **kwargs)
