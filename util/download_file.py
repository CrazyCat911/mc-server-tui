from util.client import client as c
from textual.widgets import ProgressBar


def download_file(
    url: str, path: str, progress_bar: ProgressBar = ProgressBar()
) -> None:
    chunk_size = 10 * 1024

    with c.stream("GET", url) as response:
        response.raise_for_status()

        content_length = response.headers.get("content-length")
        progress_bar.total = (
            float(content_length) if content_length is not None else None
        )

        with open(path, "xb") as file:
            for chunk in response.iter_bytes(chunk_size=chunk_size):
                file.write(chunk)
                progress_bar.advance(len(chunk))
