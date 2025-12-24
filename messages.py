from rich.text import Text

SETUP_SHORT = "Setup"
SETUP_LONG = "Server Setup"

SERVER_EXISTS = """# Server already exists"""
VANILLA_DESCRIPTION = Text.from_markup(
    "[white b]Vanilla[/] [bright_black i]The official Mojang-approved server[/]"
)
FABRIC_DESCRIPTION = Text.from_markup(
    "[light_yellow3 b]Fabric[/] [bright_black i]A fast modding framework[/]"
)
QUILT_DESCRIPTION = Text.from_markup(
    "[purple b]Quilt[/] [bright_black i]A fork of [light_yellow3]Fabric[/][/]"
)
FORGE_DESCRIPTION = Text.from_markup(
    "[grey27 b]Forge[/] [bright_black i]The OG. Very Slow and Clunky[/]"
)
NEOFORGED_DESCRIPTION = Text.from_markup(
    "[dark_orange3 b]NeoForged[/] [bright_black i]The new [grey27]Forge[/]. Much better"
)
