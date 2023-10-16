from dataclasses import dataclass
from functools import partial
import typing as T

from IPython.display import clear_output, display_html, display_markdown
import markdown

from ..agents.base import Agent


echo_md = partial(display_markdown, raw=True)
echo_html = partial(display_html, raw=True)
md2html = partial(markdown.markdown, extensions=["fenced_code"])


class NbUISkinBars:
    style = """
        <style>
            .GA20_Message {
                border: 1px solid rgba(255,255,255,0);
                margin: 0 0 6px 0;
            }
            .GA20_Message > div {
                border-style: solid;
                border-width: 0 0 0 4px;
                padding: 4px 6px;
            }
            .GA20_MessageUser > div {
                border-color: rgba(150,150,150,0.5);
                margin-left: 4px;
                opacity: 0.8;
            }
            .GA20_MessageAgent > div {
                border-color: rgba(50,200,100,0.5);
            }
            .GA20_MessageContext > div {
                border-color: rgb(50,150,220);
            }
            .GA20_MessageExample > div {
                border-color: rgba(200,200,50,0.75);
            }
            .GA20_Message:hover {
                border-color: orange;
            }
            .GA20_Message pre {
                padding: 6px 6px 8px 6px;
                border: 1px solid #ee82eeba;
            }
        </style>
    """
    msg_user = """
        <div class="GA20_Message GA20_MessageUser">
            <div>{msg}</div>
        </div>
    """
    msg_bot = """
        <div class="GA20_Message GA20_MessageAgent">
            <div>{msg}</div>
        </div>
    """
    msg_context = """
        <div class="GA20_Message GA20_MessageContext">
            <div>{msg}</div>
        </div>
    """
    msg_example = """
        <div class="GA20_Message GA20_MessageExample">
            <div>{msg}</div>
        </div>
    """
    hsep = ""


@dataclass
class AgentNbUI:
    agent: Agent

    skin = NbUISkinBars

    def ask(
        self,
        text: str,
        *,
        skip_history=False,
        native_display=True,
        **params
    ) -> None:
        out = self.agent.ask(text, skip_history=skip_history, **params)
        self.last_r_ = out
        self._echo_msg_agent(out, native_display)
        
    def askr(
        self,
        text: str,
        *,
        skip_history=False,
        **params
    ) -> str:
        out = self.agent.ask(text, skip_history=skip_history, **params)
        return out
            
    def asks(
        self,
        text: str,
        *,
        skip_history=False,
        native_display=True,
        **params
    ) -> None:
        out = self.agent.asks(text, skip_history=skip_history, **params)
        for r in out:
            clear_output(wait=True)
            self._echo_msg_agent(r, native_display)
            self.last_r_ = r
                

    def show_conversation(self) -> None:
        c = self.agent.conversation
        out = ""
        if c.context_prompt:
            msg_html = md2html("**Context/system prompt:** " + c.context_prompt)
            out += self.skin.msg_context.format(msg=msg_html + self.skin.hsep)
        if c.examples:
            for e in c.examples:
                msg_html = md2html(
                    "**Example input:** "
                    + e[0]
                    + "\n\n"
                    + "**Example output:** "
                    + e[1]
                    + "\n\n"
                )
                out += self.skin.msg_example.format(msg=msg_html + self.skin.hsep)
        for i, m in enumerate(c.messages or ()):
            if m.author == "user":
                out += self.skin.msg_user.format(msg=md2html(m.content))
            else:
                out += self.skin.msg_bot.format(msg=md2html(m.content))
        echo_html(self.skin.style + "\n" + out)

    def _echo_msg_agent(self, msg_md, native_display) -> None:
        if native_display:
            echo_md(msg_md)
        else:
            msg_html = md2html(msg_md)
            html = self.skin.style + "\n" + self.skin.msg_bot.format(msg=msg_html)
            echo_html(html)
