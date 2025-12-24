from textual.containers import VerticalScroll, Vertical
from textual.app import ComposeResult
from textual.events import Show
from textual.widgets import Markdown, RadioSet, RadioButton
from textual.reactive import reactive
import messages
from util.server_exists import server_exists


class VanillaSetup(Vertical):
    pass


class FabricSetup(Vertical):
    pass


class QuiltSetup(Vertical):
    pass


class ForgeSetup(Vertical):
    pass


class NeoForgedSetup(Vertical):
    pass


class SetupForm(Vertical):
    mod_loader: reactive[None | str] = reactive(None)

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.radio_set == self.query_one("#mod-loader-form", RadioSet):
            self.mod_loader = event.pressed.name
            event.radio_set.disabled = True

    def watch_mod_loader(self, mod_loader):
        match mod_loader:
            case "vanilla":
                self.mount(VanillaSetup())
            case "fabric":
                self.mount(FabricSetup())
            case "quilt":
                self.mount(QuiltSetup())
            case "forge":
                self.mount(ForgeSetup())
            case "neoforged":
                self.mount(NeoForgedSetup())

    def validate_mod_loader(self, mod_loader: str | None):
        if mod_loader not in {"vanilla", "fabric", "quilt", "forge", "neoforged"}:
            return None
        return mod_loader

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
        self.query_one("#mod-loader-form", RadioSet).focus()

    def compose(self) -> ComposeResult:
        if server_exists("."):
            yield Markdown(messages.SERVER_EXISTS)
        else:
            yield SetupForm()
