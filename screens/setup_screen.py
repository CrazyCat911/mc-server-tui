from textual.containers import VerticalScroll, Vertical
from textual.app import ComposeResult
from textual.widgets import Markdown, RadioSet, RadioButton
import messages
from util.server_exists import server_exists


class SetupScreen(VerticalScroll):
    CSS_PATH = "setup_screen.tcss"

    def compose(self) -> ComposeResult:
        if False:  # server_exists(".")
            yield Markdown(messages.SERVER_EXISTS)
        else:
            yield SetupForm()


class SetupForm(Vertical):
    def compose(self) -> ComposeResult:
        with RadioSet():
            yield RadioButton(messages.VANILLA_DESCRIPTION)
            yield RadioButton(messages.FABRIC_DESCRIPTION)
            yield RadioButton(messages.QUILT_DESCRIPTION)
            yield RadioButton(messages.FORGE_DESCRIPTION)
            yield RadioButton(messages.NEOFORGED_DESCRIPTION)
