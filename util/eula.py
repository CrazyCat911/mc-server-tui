from jproperties import Properties


def set_eula(agreed: bool, server_path: str) -> None:
    p = Properties()

    with open(f"{server_path}/eula.txt", "rwb") as f:
        p.load(f, "utf-8")
        p["eula"] = "true" if agreed else "false"
        p.store(f, encoding="utf-8")
