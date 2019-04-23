import os
import pytest

from conftest import TESTS_DIR
from streamer.main import get_app


@pytest.fixture(scope="session")
def storage():
    return os.path.join(TESTS_DIR, "test-files", "test-photos")


@pytest.fixture(scope="function")
def app(storage):
    return get_app(storage)


async def test_index(aiohttp_client, app):
    client = await aiohttp_client(app)
    resp = await client.get("/")
    assert resp.status == 200
    text = await resp.text()
    assert "Микросервис для скачивания файлов" in text


async def test_archivate_bad_request(aiohttp_client, app):
    client = await aiohttp_client(app)
    resp = await client.get("/archive/7kna../")
    assert resp.status == 400
    resp = await client.get("/archive/7k-na/")
    assert resp.status == 400


async def test_archivate_not_found(aiohttp_client, app):
    client = await aiohttp_client(app)
    resp = await client.get("/archive/7knb/")
    assert resp.status == 404


async def test_archivate_ok(aiohttp_client, app):
    client = await aiohttp_client(app)
    resp = await client.get("/archive/7kna/")
    assert resp.status == 200
    await resp.read()
