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
        yield Button("Info", id="btn-info")
        yield Button("Setup", id="btn-setup")
        yield Button("Mods", id="btn-mods")
        yield Button("Console", id="btn-console")
        yield Button("Settings", id="btn-settings")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()
        self.current_menu = (
            event.button.id.replace("btn-", "view-")
            if event.button.id
            else self.current_menu
        )
        self.post_message(self.MenuChanged(self.current_menu))

    def watch_current_menu(self, current_menu: str) -> None:
        button_id = current_menu.replace("view-", "btn-")
        for button in self.query(Button):
            if button.id == button_id:
                button.variant = "primary"
            else:
                button.variant = "default"


class MCServerTui(App):
    """A Minecraft Server TUI"""

    CSS_PATH = "main.tcss"
    TITLE = "Minecraft Server Manager"
    SUB_TITLE = "!!! WORK IN PROGRESS !!!"
    BINDINGS = [
        ("1", "switch_menu('view-info')", "Info"),
        ("2", "switch_menu('view-setup')", "Setup"),
        ("3", "switch_menu('view-mods')", "Mods"),
        ("4", "switch_menu('view-console')", "Console"),
        ("5", "switch_menu('view-settings')", "Settings"),
    ]

    current_menu = reactive("view-info")

    def on_mount(self) -> None:
        self.theme = "dracula"

    def on_sidebar_menu_changed(self, event: Sidebar.MenuChanged) -> None:
        self.current_menu = event.new_menu

    def watch_current_menu(self, current_menu: str) -> None:
        self.query_one(ContentSwitcher).current = current_menu
        sidebar = self.query_one(Sidebar)
        sidebar.current_menu = current_menu

    def action_switch_menu(self, menu: str) -> None:
        self.current_menu = menu

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Horizontal():
            yield Sidebar()
            with ContentSwitcher(initial="view-info", id="main"):
                yield Placeholder("Info", id="view-info")
                yield Placeholder("Setup", id="view-setup")
                yield Placeholder("Mods", id="view-mods")
                yield Placeholder("Console", id="view-console")
                yield Placeholder("Settings", id="view-settings")


if __name__ == "__main__":
    app = MCServerTui()
    app.run()
