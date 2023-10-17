"""Use a single chain to route an input to one of multiple llm chains."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from promptmanager.script.base.chains import ConversationChain
from promptmanager.script.base.chains.base import Chain
from promptmanager.script.base.chains.llm import LLMChain
from promptmanager.script.base.chains.router.base import MultiRouteChain
from promptmanager.script.base.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from promptmanager.script.base.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from promptmanager.script.base.prompts import PromptTemplate
from promptmanager.script.base.schema.language_model import BaseLanguageModel


class MultiPromptChain(MultiRouteChain):
    """A multi-route chain that uses an LLM router chain to choose amongst prompts."""

    @property
    def output_keys(self) -> List[str]:
        return ["text"]

    @classmethod
    def from_prompts(
        cls,
        llm: BaseLanguageModel,
        prompt_infos: List[Dict[str, str]],
        default_chain: Optional[Chain] = None,
        **kwargs: Any,
    ) -> MultiPromptChain:
        """Convenience constructor for instantiating from destination prompts."""
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = "\n".join(destinations)
        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
            destinations=destinations_str
        )
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )
        router_chain = LLMRouterChain.from_llm(llm, router_prompt)
        destination_chains = {}
        for p_info in prompt_infos:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = PromptTemplate(template=prompt_template, input_variables=["input"])
            chain = LLMChain(llm=llm, prompt=prompt)
            destination_chains[name] = chain
        _default_chain = default_chain or ConversationChain(llm=llm, output_key="text")
        return cls(
            router_chain=router_chain,
            destination_chains=destination_chains,
            default_chain=_default_chain,
            **kwargs,
        )
