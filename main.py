from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Footer, ContentSwitcher, Button, Placeholder
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.message import Message


class Sidebar(Vertical):
    class MenuChanged(Message):
        def __init__(self, new_menu: str) -> None:
            super().__init__()
            self.new_menu = new_menu

    current_menu = reactive("view-info")

    def compose(self) -> ComposeResult:
        yield Button("info", id="btn-info")
        yield Button("setup", id="btn-setup")
        yield Button("mods", id="btn-mods")
        yield Button("console", id="btn-console")
        yield Button("settings", id="btn-settings")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()
        self.current_menu = (
            event.button.id.replace("btn-", "view-")
            if event.button.id
            else self.current_menu
        )
        self.post_message(self.MenuChanged(self.current_menu))

    def watch_current_menu(self, current_menu: str) -> None:
        pass  # TODO: Replace with button style switching code


class MCServerTui(App):
    """A Minecraft Server TUI"""

    CSS_PATH = "main.tcss"
    TITLE = "Minecraft Server Manager"
    SUB_TITLE = "!!! WORK IN PROGRESS !!!"

    current_menu = reactive("view-info")

    def on_mount(self) -> None:
        self.theme = "dracula"

    def on_sidebar_menu_changed(self, event: Sidebar.MenuChanged) -> None:
        self.current_menu = event.new_menu

    def watch_current_menu(self, current_menu: str) -> None:
        self.query_one(ContentSwitcher).current = current_menu

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Horizontal():
            yield Sidebar()
            with ContentSwitcher(initial="view-info", id="main"):
                yield Placeholder("info", id="view-info")
                yield Placeholder("setup", id="view-setup")
                yield Placeholder("mods", id="view-mods")
                yield Placeholder("console", id="view-console")
                yield Placeholder("settings", id="view-settings")


if __name__ == "__main__":
    app = MCServerTui()
    app.run()
