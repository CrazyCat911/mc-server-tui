from packaging import version
from util.client import client as c
from util.download_file import download_file
import os, shutil
from textual.widgets import ProgressBar


""" VANILLA """

VANILLA_URL = "https://launchermeta.mojang.com"


async def get_supported_vanilla_game_versions() -> list[str]:
    supported_versions: list[str] = []
    response = await c.get(f"{VANILLA_URL}/mc/game/version_manifest.json", timeout=5)
    data: dict = response.json()
    for obj in data["versions"]:
        if obj["type"] == "snapshot":
            supported_versions.append(obj["id"])
        elif obj["type"] == "release":
            if version.parse(obj["id"]) >= version.parse(
                "1.2.5"
            ):  # 1.2.5 is the version that added server jars
                supported_versions.append(obj["id"])

    return supported_versions


async def get_vanilla_server_download_url(version: str) -> str:
    response = await c.get(f"{VANILLA_URL}/mc/game/version_manifest.json", timeout=5)
    data = response.json()

    version_url: str | None = None

    for version_meta in data["versions"]:
        if version_meta["id"] == version:
            version_url = version_meta["url"]
            break

    if not version_url:
        raise Exception(f"Version {version} not found")

    response = await c.get(version_url, timeout=5)
    data = response.json()

    download_url = data["downloads"]["server"]["url"]

    return download_url


async def install_vanilla_server(version: str, path: str, progress_bar: ProgressBar):
    await download_file(
        await get_vanilla_server_download_url(version), path, progress_bar
    )


""" FABRIC """

FABRIC_URL = "https://meta.fabricmc.net"


async def get_supported_fabric_game_versions() -> list[str]:
    response = await c.get(
        f"{FABRIC_URL}/v2/versions/game", timeout=5
    )  # see https://github.com/FabricMC/fabric-meta?tab=readme-ov-file#v2versionsgame
    data: list[dict] = response.json()
    return [obj["version"] for obj in data]


async def get_supported_fabric_versions(game_version: str) -> list[str]:
    response = await c.get(
        f"{FABRIC_URL}/v2/versions/loader/{game_version}", timeout=5
    )  # See https://github.com/FabricMC/fabric-meta?tab=readme-ov-file#v2versionsloadergame_version
    data: list[dict] = response.json()
    return [obj["loader"]["version"] for obj in data]


async def get_fabric_installer_versions() -> list[str]:
    response = await c.get(f"{FABRIC_URL}/v2/versions/installer", timeout=5)
    data: list[dict] = response.json()
    return [obj["version"] for obj in data]


async def get_fabric_server_download_url(
    game_version: str, loader_version: str, installer_version: str
) -> str:
    return f"{FABRIC_URL}/v2/versions/loader/{game_version}/{loader_version}/{installer_version}/server/jar"


async def install_fabric_server(
    game_version: str,
    loader_version: str,
    installer_version: str,
    path: str,
    progress_bar: ProgressBar,
):
    await download_file(
        await get_fabric_server_download_url(
            game_version, loader_version, installer_version
        ),
        path,
        progress_bar,
    )


""" QUILT """

QUILT_URL = "https://meta.quiltmc.org"


async def get_supported_quilt_game_versions() -> list[str]:
    response = await c.get(
        f"{QUILT_URL}/v3/versions/game", timeout=5
    )  # see https://meta.quiltmc.org/#/v3/get_v3_versions_game
    data: list[dict] = response.json()
    return [obj["version"] for obj in data]


async def get_quilt_installer_versions() -> list[str]:
    response = await c.get(f"{QUILT_URL}/v3/versions/installer", timeout=5)
    data: list[dict] = response.json()
    return [obj["version"] for obj in data]


async def get_quilt_download_url(version: str) -> str:
    response = await c.get(f"{QUILT_URL}/v3/versions/installer", timeout=5)
    data: list[dict] = response.json()
    for obj in data:
        if obj["version"] == version:
            return obj["url"]

    raise Exception("Version not found")


async def download_quilt_installer(
    version: str, path: str, progress_bar: ProgressBar
) -> None:
    await download_file(await get_quilt_download_url(version), path, progress_bar)


def install_quilt_server(
    installer_path: str, game_version: str, server_path: str
) -> None:
    os.system(
        f"""java -jar {installer_path} \\
        install server {game_version} \\
        --download-server"""
    )

    shutil.move("./server/", server_path)
