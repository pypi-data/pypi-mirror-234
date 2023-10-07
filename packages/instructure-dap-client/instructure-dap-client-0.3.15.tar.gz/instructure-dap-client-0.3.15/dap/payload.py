import io
import zlib
from typing import AsyncIterator

import aiohttp


async def get_lines_from_gzip_stream(
    stream: aiohttp.StreamReader,
) -> AsyncIterator[bytes]:
    "Extracts lines from a gzipped HTTP payload stream."

    # use a special value for wbits (windowBits) to indicate gzip compression
    # see: https://docs.python.org/3/library/zlib.html#zlib.decompress
    decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)

    buf = io.BytesIO()
    compressed_data: bytes

    while True:
        compressed_data = await stream.read(64 * 1024)
        if not compressed_data:
            break

        data = decompressor.decompress(compressed_data)

        start: int = 0
        while True:
            # find newline character
            end: int = data.find(10, start)
            if end >= 0:  # has newline, process data
                buf.write(data[start:end])
                buf.seek(0, io.SEEK_SET)
                yield buf.getvalue()
                buf = io.BytesIO()
                start = end + 1
            else:  # has no newline, read more data
                buf.write(data[start:])
                break

    # process remaining data
    rem = buf.getvalue()
    if rem:
        yield rem
