from typing import Sequence, TypedDict

from promptmanager.script.base.schema import BaseMessage


class ChatSession(TypedDict, total=False):
    """Chat Session represents a single
    conversation, channel, or other group of messages."""

    messages: Sequence[BaseMessage]
    """The Promptmanager chat messages loaded from the source."""
    functions: Sequence[dict]
    """The function calling specs for the messages."""
