import typing as t
from typing import Literal

from pydantic import BaseModel

from lifeomic_chatbot_tools.types.conversations.actions import AgentAction, HumanAgentAction, UserAction


class DialogueState(BaseModel):
    slotValues: t.Dict[str, t.Any]


class BaseDialogueTurn(BaseModel):
    state: t.Optional[DialogueState] = None


class UserDialogueTurn(BaseDialogueTurn):
    userAction: UserAction
    actor: Literal["USER"] = "USER"


class AgentDialogueTurn(BaseDialogueTurn):
    agentAction: AgentAction
    actor: Literal["AGENT"] = "AGENT"


class HumanAgentDialogueTurn(BaseDialogueTurn):
    humanAgentAction: HumanAgentAction
    actor: Literal["HUMAN_AGENT"] = "HUMAN_AGENT"


DialogueTurn = t.Union[AgentDialogueTurn, HumanAgentDialogueTurn, UserDialogueTurn]
