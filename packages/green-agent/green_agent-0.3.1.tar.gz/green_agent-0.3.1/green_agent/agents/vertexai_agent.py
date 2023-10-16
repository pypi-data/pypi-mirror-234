from copy import deepcopy
import typing as T

import vertexai.language_models as vxlm

from .base import Agent, Conversation, Message


class VertexAIAgent(Agent):
    conversation: Conversation
    params: dict

    _model: vxlm.ChatModel
    _chat_session: vxlm.ChatSession = None

    def __init__(
      self,
      context_prompt: str = '', *,
      conversation: Conversation | None = None,
      **params
    ):
        if conversation is not None:
          assert not context_prompt
        else:
          assert context_prompt is not None
          conversation = Conversation(
              context_prompt=context_prompt,
              messages=[]
          )
        self.conversation = conversation
        self._model = vxlm.ChatModel.from_pretrained(params.pop("model"))
        self.params = params

    def ask(
        self, text: str, *, skip_history=False, **params
    ) -> str:
        new_messages = deepcopy(self.conversation.messages)
        new_messages.append(Message("user", text))

        chat_session = self._get_chat_session()

        send_message_args = {
            **self.params,
            **params,
        }
        self.last_res_ = chat_session.send_message(text, **send_message_args)

        out = self.last_res_.text
        assert out is not None

        if not skip_history:
            new_messages.append(Message("bot", out))
            self.conversation.messages = new_messages

        return out

    def _get_chat_session(self):
        if self._chat_session is None:
            self._chat_session = self._model.start_chat(
                context=self.conversation.context_prompt,
                examples=[
                    vxlm.InputOutputTextPair(input_text=e[0], output_text=e[1])
                    for e in self.conversation.examples
                ] if self.conversation.examples else None,
                message_history=self._make_api_messages(self.conversation.messages)
                    if self.conversation.messages else None,
                **self.params,
            )
        return self._chat_session

    def _make_api_messages(self, messages: list[Message]) -> list[dict]:
        return [vars(m) for m in messages]
