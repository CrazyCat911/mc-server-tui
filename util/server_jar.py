import requests
from packaging import version
from req_session import session as s

SUPPORTED_LOADERS = {"vanilla", "fabric", "quilt"}


def get_supported_game_versions(loader: str) -> list[str]:
    if loader not in SUPPORTED_LOADERS:
        raise ValueError(f"Unsupported mod loader: {loader}")

    supported_versions = []

    if loader == "vanilla":
        response = s.get(
            "https://launchermeta.mojang.com/mc/game/version_manifest.json", timeout=5
        )
        vanilla_data: dict = response.json()
        for vanilla_version in vanilla_data["versions"]:
            if vanilla_version["type"] == "snapshot":
                supported_versions.append(vanilla_version["id"])
            elif vanilla_version["type"] == "release":
                if version.parse(vanilla_version["id"]) >= version.parse(
                    "1.2.5"
                ):  # 1.2.5 is the version that added server jars
                    supported_versions.append(vanilla_version["id"])

    elif loader == "fabric":
        response = s.get(
            "https://meta.fabricmc.net/v2/versions/game", timeout=5
        )  # see https://github.com/FabricMC/fabric-meta?tab=readme-ov-file#v2versionsgame
        fabric_data: list[dict] = response.json()
        supported_versions = [
            fabric_version["version"] for fabric_version in fabric_data
        ]

    elif loader == "quilt":
        response = s.get(
            "https://meta.quiltmc.org/v3/versions/game", timeout=5
        )  # see https://meta.quiltmc.org/#/v3/get_v3_versions_game
        quilt_data: list[dict] = response.json()
        supported_versions = [quilt_version["version"] for quilt_version in quilt_data]

    return supported_versions


def get_supported_loader_versions(game_version: str, loader: str) -> list[str]:
    if loader not in SUPPORTED_LOADERS:
        raise ValueError(f"Unsupported mod loader: {loader}")

    supported_versions: list[str] = []

    if loader == "vanilla":
        supported_versions = [game_version]

    elif loader == "fabric":
        response = s.get(
            f"https://meta.fabricmc.net/v2/versions/loader/{game_version}", timeout=5
        )  # See https://github.com/FabricMC/fabric-meta?tab=readme-ov-file#v2versionsloadergame_version
        fabric_data: list[dict] = response.json()
        supported_versions = [obj["loader"]["version"] for obj in fabric_data]

    elif loader == "quilt":
        response = s.get(
            f"https://meta.quiltmc.org/v3/versions/loader/{game_version}", timeout=5
        )  # See https://meta.quiltmc.org/#/v3/get_v3_versions_loader__game_version_
        quilt_data = response.json()
        supported_versions = [obj["loader"]["version"] for obj in quilt_data]

    return supported_versions
