"""Models for the Constitutional AI chain."""
from promptmanager.script.base.pydantic_v1 import BaseModel


class ConstitutionalPrinciple(BaseModel):
    """Class for a constitutional principle."""

    critique_request: str
    revision_request: str
    name: str = "Constitutional Principle"
