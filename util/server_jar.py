import requests
from packaging import version
from req_session import session as s

""" VANILLA """

VANILLA_URL = "https://launchermeta.mojang.com"


def get_supported_vanilla_game_versions() -> list[str]:
    supported_versions: list[str] = []
    response = s.get(f"{VANILLA_URL}/mc/game/version_manifest.json", timeout=5)
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


def get_vanilla_server_download_url(version: str, filepath: str) -> str:
    response = s.get(f"{VANILLA_URL}/mc/game/version_manifest.json", timeout=5)
    data = response.json()

    version_url: str | None = None

    for version_meta in data["versions"]:
        if version_meta["id"] == version:
            version_url = version_meta["url"]
            break

    if not version_url:
        raise Exception(f"Version {version} not found")

    response = s.get(version_url, timeout=5)
    data = response.json()

    download_url = data["downloads"]["server"]["url"]

    return download_url


""" FABRIC """

FABRIC_URL = "https://meta.fabricmc.net"


def get_supported_fabric_game_versions() -> list[str]:
    response = s.get(
        f"{FABRIC_URL}/v2/versions/game", timeout=5
    )  # see https://github.com/FabricMC/fabric-meta?tab=readme-ov-file#v2versionsgame
    data: list[dict] = response.json()
    return [obj["version"] for obj in data]


def get_supported_fabric_versions(game_version: str) -> list[str]:
    response = s.get(
        f"{FABRIC_URL}/v2/versions/loader/{game_version}", timeout=5
    )  # See https://github.com/FabricMC/fabric-meta?tab=readme-ov-file#v2versionsloadergame_version
    data: list[dict] = response.json()
    return [obj["loader"]["version"] for obj in data]


def get_fabric_installer_versions() -> list[str]:
    response = s.get(f"{FABRIC_URL}/v2/versions/installer", timeout=5)
    data: list[dict] = response.json()
    return [obj["version"] for obj in data]


""" QUILT """

QUILT_URL = "https://meta.quiltmc.org"


def get_supported_quilt_game_versions() -> list[str]:
    response = s.get(
        f"{QUILT_URL}/v3/versions/game", timeout=5
    )  # see https://meta.quiltmc.org/#/v3/get_v3_versions_game
    data: list[dict] = response.json()
    return [obj["version"] for obj in data]


def get_supported_quilt_versions(game_version: str) -> list[str]:
    response = s.get(
        f"{QUILT_URL}/v3/versions/loader/{game_version}", timeout=5
    )  # See https://meta.quiltmc.org/#/v3/get_v3_versions_loader__game_version_
    data = response.json()
    return [obj["loader"]["version"] for obj in data]
