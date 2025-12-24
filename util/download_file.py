from req_session import session as s
from textual.widgets import ProgressBar


def download_file(
    url: str, path: str, progress_bar: ProgressBar = ProgressBar()
) -> None:
    response = s.get(url, stream=True)
    chunk_size = 10 * 1024

    content_length = response.headers.get("content-length")
    progress_bar.total = float(content_length) if content_length is not None else None

    with open(path, "xb") as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
            progress_bar.advance(chunk_size)
