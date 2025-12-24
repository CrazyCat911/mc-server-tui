from pathlib import Path


def server_exists(path) -> bool:
    server_path = Path(f"{path}/server.jar")

    return server_path.exists()
