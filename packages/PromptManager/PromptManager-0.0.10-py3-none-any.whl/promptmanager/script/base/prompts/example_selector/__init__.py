"""Logic for selecting examples to include in prompts."""
from promptmanager.script.base.prompts.example_selector.length_based import LengthBasedExampleSelector
from promptmanager.script.base.prompts.example_selector.ngram_overlap import NGramOverlapExampleSelector
from promptmanager.script.base.prompts.example_selector.semantic_similarity import (
    MaxMarginalRelevanceExampleSelector,
    SemanticSimilarityExampleSelector,
)

__all__ = [
    "LengthBasedExampleSelector",
    "MaxMarginalRelevanceExampleSelector",
    "NGramOverlapExampleSelector",
    "SemanticSimilarityExampleSelector",
]
