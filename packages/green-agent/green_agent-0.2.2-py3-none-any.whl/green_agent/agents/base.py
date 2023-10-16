from copy import deepcopy
from dataclasses import dataclass
import typing as T


@dataclass
class Message:
    # eg. OpenAI "role" ("system", "user" or "assistant")
    # or Vertex/Google "author" ("user" or "bot")
    author: T.Literal["user", "bot"]
    content: str


@dataclass
class Conversation:
    messages: list[Message]
    # eg. OpenAI "system prompt" or Vertex/Google "context"
    context_prompt: str | None = None
    # list of ("input", "output") pairs
    examples: list[tuple[str, str]] | None = None


class Agent:
    conversation: Conversation = None

    def ask(
        self, text: str, *, skip_history=False, **params
    ) -> str:
        raise NotImplementedError

    def clone(self) -> "Agent":
        return deepcopy(self)
