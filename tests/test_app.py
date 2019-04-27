import io
import os
import zipfile
from types import SimpleNamespace

import pytest

from conftest import TESTS_DIR
from streamer.main import get_app


@pytest.fixture(scope="session")
def storage():
    return os.path.join(TESTS_DIR, "test-files", "test-photos")


@pytest.fixture(scope="session")
def args(storage):
    """args object mock"""
    return SimpleNamespace(archive=storage, delay=0)


@pytest.fixture(scope="function")
def app(args):
    return get_app(args)


async def test_index(aiohttp_client, app):
    client = await aiohttp_client(app)
    resp = await client.get("/")
    assert resp.status == 200
    text = await resp.text()
    assert "Микросервис для скачивания файлов" in text


async def test_archivate_path_param_dont_match_regex(aiohttp_client, app):
    client = await aiohttp_client(app)
    resp = await client.get("/archive/7kna../")
    assert resp.status == 404
    resp = await client.get("/archive/7k-na/")
    assert resp.status == 404


async def test_archivate_not_found(aiohttp_client, app):
    client = await aiohttp_client(app)
    resp = await client.get("/archive/7knb/")
    assert resp.status == 404


async def test_archivate_ok(aiohttp_client, app):
    client = await aiohttp_client(app)
    resp = await client.get("/archive/7kna/")
    assert resp.status == 200
    archive = await resp.read()
    assert zipfile.is_zipfile(io.BytesIO(archive))


async def test_client_close_connection(aiohttp_client, app):
    """just open connection and don't read response
    there should not be warnings in console
    """
    client = await aiohttp_client(app)
    resp = await client.get("/archive/7kna/")
    assert resp.status == 200
