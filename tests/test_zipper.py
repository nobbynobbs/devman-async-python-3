import io
import zipfile

import pytest

from streamer.zipper import Zipper


@pytest.yield_fixture
async def zipper(directory_path):
    return Zipper(directory_path)


@pytest.mark.asyncio
async def test_gready_zipper(zipper, file_path, file_content):
    """read all output"""
    async with zipper:
        res = await zipper.read(0)
    z = zipfile.ZipFile(io.BytesIO(res))
    unzipped = z.read('random-bytes')
    assert unzipped == file_content


@pytest.mark.asyncio
async def test_chunked_zipper(zipper, directory_path, file_content):
    """read output by chunks"""
    res = b""
    async with zipper:
        while True:
            chunk = await zipper.read(10)
            if chunk == b"":
                break
            res += chunk
    z = zipfile.ZipFile(io.BytesIO(res))
    unzipped = z.read('random-bytes')
    assert unzipped == file_content
