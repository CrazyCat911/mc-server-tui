from textual.containers import VerticalScroll, Vertical
from textual.app import ComposeResult
from textual.events import Show
from textual.widgets import Markdown, RadioSet, RadioButton
import messages
from util.server_exists import server_exists


class SetupScreen(VerticalScroll):
    CSS_PATH = "setup_screen.tcss"
    BORDER_TITLE = messages.SETUP_LONG

    def on_show(self, event: Show) -> None:
        self.query_one("#mod-loader-form", RadioSet).focus()

    def compose(self) -> ComposeResult:
        if False:  # server_exists(".")
            yield Markdown(messages.SERVER_EXISTS)
        else:
            yield SetupForm()


class SetupForm(Vertical):
    def compose(self) -> ComposeResult:
        with RadioSet(id="mod-loader-form"):
            yield RadioButton(messages.VANILLA_DESCRIPTION)
            yield RadioButton(messages.FABRIC_DESCRIPTION)
            yield RadioButton(messages.QUILT_DESCRIPTION)
            yield RadioButton(messages.FORGE_DESCRIPTION)
            yield RadioButton(messages.NEOFORGED_DESCRIPTION)
