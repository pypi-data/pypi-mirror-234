from dataclasses import dataclass
from functools import partial

from IPython.display import display_markdown

from ..agents.base import Agent


echo_md = partial(display_markdown, raw=True)


@dataclass
class AgentNbUI:
    agent: Agent

    def ask(
        self, text: str, *, skip_history=False, display=True, **params
    ) -> str | None:
        out = self.agent.ask(text, skip_history=skip_history, **params)
        if display:
            echo_md(out)
        else:
            return out

    def show_conversation(self) -> None:
        c = self.agent.conversation
        out = ""
        if c.context_prompt:
            out += "**Context/System prompt:** " + c.context_prompt
            out += "\n\n---\n"
        if c.examples:
            out += "**Examples:**\n"
            for e in c.examples:
                out += "\n**&rarr; Input:** " + e[0]
                out += "\n**Output:** " + e[0]
            out += "\n\n---\n"
        for i, m in enumerate(c.messages or ()):
            out += f"**{m.author.capitalize()}[{i // 2}]:** {m.content}\n\n"
            if m.author != "user":
                out += "\n\n---\n"
        echo_md(out)
