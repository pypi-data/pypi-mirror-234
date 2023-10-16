from copy import deepcopy
import typing as T

import openai

from .base import Agent, Conversation, Message


class OpenAIAgent(Agent):
    conversation: Conversation
    params: dict

    def __init__(self, conversation, **params):
        self.conversation = conversation
        self.params = params

    def ask(
        self, text: str, *, skip_history=False, display=True, **params
    ) -> str:
        new_messages = deepcopy(self.conversation.messages)
        new_messages.append(Message("user", text))

        create_args = {
            **self.params,
            **params,
            "messages": self._make_api_messages(new_messages)
        }
        self.last_res_ = openai.ChatCompletion.create(**create_args)

        out = self.last_res_.choices[0].message.content
        assert out is not None

        if not skip_history:
            new_messages.append(Message("bot", out))
            self.conversation.messages = new_messages

        return out

    def _make_api_messages(self, messages: list[Message]) -> list[dict]:
        return [
            {
                "role": "assistant" if m.author == "bot" else m.author,
                "content": m.content
            }
            for m in messages
        ]
