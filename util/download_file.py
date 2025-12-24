from util.client import client as c
from textual.widgets import ProgressBar
import aiofiles


async def download_file(
    url: str, path: str, progress_bar: ProgressBar = ProgressBar()
) -> None:
    chunk_size = 10 * 1024

    async with c.stream("GET", url) as response:
        response.raise_for_status()

        content_length = response.headers.get("content-length")
        progress_bar.total = (
            float(content_length) if content_length is not None else None
        )

        async with aiofiles.open(path, "xb") as file:
            async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                await file.write(chunk)
                progress_bar.advance(len(chunk))
