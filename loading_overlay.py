from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import ProgressBar, Static
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
        self.progress_bar = progress_bar
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static(self.text)
            yield self.progress_bar
