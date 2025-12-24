from textual.app import ComposeResult, App
from textual.screen import Screen
from textual.widgets import ProgressBar, Static, Footer, Header
from textual.reactive import reactive
from textual.containers import Vertical


class LoadingOverlay(Screen):
    CSS_PATH = "loading_overlay.tcss"

    text: reactive[str] = reactive("")

    def __init__(
        self,
        text: str,
        progress_bar: ProgressBar,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.text = text
        self.progress_bar = progress_bar

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static(self.text, id="loading-overlay-description")
            yield self.progress_bar
        yield Footer()
