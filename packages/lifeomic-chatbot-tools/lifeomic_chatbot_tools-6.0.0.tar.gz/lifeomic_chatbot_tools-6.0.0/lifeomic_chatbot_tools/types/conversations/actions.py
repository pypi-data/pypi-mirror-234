import typing as t
from enum import Enum

from pydantic import BaseModel


class TagValue(BaseModel):
    """Represents a named entity's type and value."""

    tagType: str
    value: str


class Sentiment(Enum):
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"


class UserAction(BaseModel):
    """Represents any type of user action (email, utterance, option, etc)."""

    type: str
    utterance: t.Optional[str] = None
    translatedUtterance: t.Optional[str] = None
    intent: t.Optional[str] = None
    sentiment: t.Optional[Sentiment] = None
    confidence: t.Optional[float] = None
    ood: t.Optional[bool] = None
    oodConfidence: t.Optional[float] = None
    tags: t.Optional[t.List[TagValue]] = None


class AgentAction(BaseModel):
    """Represents any type of agent action (form, utterance, email, etc.)"""

    type: str
    name: str  # the action's name
    utterance: t.Optional[str] = None
    requiredSlots: t.Optional[t.List[str]] = None


class HumanAgentAction(BaseModel):
    type: str
    utterance: t.Optional[str]
