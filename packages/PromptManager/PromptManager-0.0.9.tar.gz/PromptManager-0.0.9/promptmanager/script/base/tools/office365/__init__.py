"""O365 tools."""

from promptmanager.script.base.tools.office365.create_draft_message import O365CreateDraftMessage
from promptmanager.script.base.tools.office365.events_search import O365SearchEvents
from promptmanager.script.base.tools.office365.messages_search import O365SearchEmails
from promptmanager.script.base.tools.office365.send_event import O365SendEvent
from promptmanager.script.base.tools.office365.send_message import O365SendMessage
from promptmanager.script.base.tools.office365.utils import authenticate

__all__ = [
    "O365SearchEmails",
    "O365SearchEvents",
    "O365CreateDraftMessage",
    "O365SendMessage",
    "O365SendEvent",
    "authenticate",
]
