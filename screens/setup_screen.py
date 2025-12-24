from textual.containers import VerticalScroll, Vertical, Horizontal
from textual.app import ComposeResult
from textual.events import Mount, Show
from textual import work
from textual.widget import Widget
from textual.widgets import (
    Markdown,
    RadioSet,
    RadioButton,
    Select,
    ProgressBar,
    Button,
)
from textual.reactive import reactive
from textual.message import Message
import messages
from util.server_exists import server_exists
import util.server_jar
from loading_overlay import LoadingOverlay


class ModLoaderSetup(Vertical):
    DEFAULT_CSS = """
    ModLoaderSetup {
        align: center top;
        margin: 1;
    }
    """

    class Canceled(Message):
        def __init__(self) -> None:
            super().__init__()


class VanillaSetup(ModLoaderSetup):
    game_versions: reactive[list[str]] = reactive([], recompose=True)

    @work(exclusive=True)
    async def get_info(self):
        self.loading = True
        try:
            self.game_versions = (
                await util.server_jar.get_supported_vanilla_game_versions()
            )
        except Exception as error:
            self.notify(
                messages.VANILLA_GAME_VERSION_ERROR,
                title=messages.VANILLA_GAME_VERSION_ERROR_TITLE,
                severity="error",
            )
            self.log.error(error)
            self.post_message(self.Canceled())
        finally:
            self.loading = False

    @work(exclusive=True)
    async def setup_server(self):
        try:
            select_value = self.query_one(Select).value
            if select_value != Select.BLANK:
                version: str = select_value
                progress_bar = ProgressBar()
                self.app.push_screen(
                    LoadingOverlay("Installing Vanilla Server", progress_bar)
                )
                await util.server_jar.install_vanilla_server(
                    version, "./server.jar", progress_bar
                )
        except Exception as error:
            self.notify("Error", severity="error")
            self.log.error(error)

    def compose(self) -> ComposeResult:
        yield Select(
            ((v, v) for v in self.game_versions),
            id="game-version-select",
        )
        with Horizontal():
            yield Button("Cancel", variant="error", id="cancel-button")
            yield Button(
                "Confirm", variant="success", id="confirm-button", disabled=True
            )

    def on_mount(self) -> None:
        self.get_info()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-button":
            event.stop()
            self.post_message(self.Canceled())
        elif event.button.id == "confirm-button":
            self.setup_server()

    def on_select_changed(self, event: Select.Changed):
        confirm_button = self.query_one("#confirm-button", Button)
        if event.value != Select.BLANK:
            confirm_button.disabled = False
        else:
            confirm_button.disabled = True


class FabricSetup(ModLoaderSetup):
    pass


class QuiltSetup(ModLoaderSetup):
    pass


class ForgeSetup(ModLoaderSetup):
    pass


class NeoForgedSetup(ModLoaderSetup):
    pass


class SetupForm(Vertical):
    mod_loader: reactive[None | str] = reactive(None)
    can_focus = True

    def __init__(
        self,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True,
    ) -> None:
        super().__init__(
            *children,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
            markup=markup,
        )

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.radio_set == self.query_one("#mod-loader-form", RadioSet):
            self.mod_loader = event.pressed.name
            event.radio_set.disabled = True

    def watch_mod_loader(self, mod_loader):
        match mod_loader:
            case "vanilla":
                self.mount(VanillaSetup(id="mod-loader-setup"))
            case "fabric":
                self.mount(FabricSetup(id="mod-loader-setup"))
            case "quilt":
                self.mount(QuiltSetup(id="mod-loader-setup"))
            case "forge":
                self.mount(ForgeSetup(id="mod-loader-setup"))
            case "neoforged":
                self.mount(NeoForgedSetup(id="mod-loader-setup"))

    def validate_mod_loader(self, mod_loader: str | None):
        if mod_loader not in {"vanilla", "fabric", "quilt", "forge", "neoforged"}:
            return None
        return mod_loader

    async def on_mod_loader_setup_canceled(self, event: ModLoaderSetup.Canceled):
        await self.recompose()

    def on_focus(self):
        self.query_one("#mod-loader-form", RadioSet).focus()

    def compose(self) -> ComposeResult:
        with RadioSet(id="mod-loader-form"):
            yield RadioButton(messages.VANILLA_DESCRIPTION, name="vanilla")
            yield RadioButton(messages.FABRIC_DESCRIPTION, name="fabric")
            yield RadioButton(messages.QUILT_DESCRIPTION, name="quilt")
            yield RadioButton(messages.FORGE_DESCRIPTION, name="forge")
            yield RadioButton(messages.NEOFORGED_DESCRIPTION, name="neoforged")


class SetupScreen(VerticalScroll):
    CSS_PATH = "setup_screen.tcss"
    BORDER_TITLE = messages.SETUP_LONG

    def on_show(self, event: Show) -> None:
        for result in self.query(SetupForm):
            result.focus()

    def compose(self) -> ComposeResult:
        if server_exists("."):
            yield Markdown(messages.SERVER_EXISTS)
        else:
            yield SetupForm()
