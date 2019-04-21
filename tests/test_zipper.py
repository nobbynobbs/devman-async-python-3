import io
import zipfile

import pytest

from streamer.zipper import Zipper


@pytest.yield_fixture
async def zipper(file_path):
    zipper = Zipper(file_path)
    await zipper.init()
    yield zipper
    await zipper.wait()


@pytest.mark.asyncio
async def test_gready_zipper(zipper, file_path, file_content):
    """read all output"""
    res = await zipper.read(0)
    z = zipfile.ZipFile(io.BytesIO(res))
    unzipped = z.read(file_path[1:])
    assert unzipped == file_content


@pytest.mark.asyncio
async def test_chunked_zipper(zipper, file_path, file_content):
    """read output by chunks"""
    res = b""
    while True:
        chunk = await zipper.read(10)
        if chunk == b"":
            break
        res += chunk
    z = zipfile.ZipFile(io.BytesIO(res))
    unzipped = z.read(file_path[1:])
    assert unzipped == file_content
