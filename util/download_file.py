from req_session import session as s


def download_file(url: str, path: str):
    response = s.get(url, stream=True)

    with open(path, "wbx") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)
