#!/usr/bin/env python3

import asyncio
import argparse
import logging
import os

import aiofiles
from aiohttp import web

from streamer.zipper import Zipper
import streamer.settings as settings


def parse_args():
    parser = argparse.ArgumentParser(
        description="aiohttp based streaming service"
    )
    parser.add_argument(
        "-s", "--storage", required=True, type=str,
        help="path to file containing directory"
    )
    args = parser.parse_args()
    return args


async def archivate(request):
    dirname = request.match_info["hash"]  # type: str
    logging.debug("Accepting request...")
    base_path = request.app["storage"]
    full_path = os.path.join(base_path, dirname)
    if os.path.isdir(full_path):
        response = web.StreamResponse(
            headers={
                "Content-Disposition": 'attachment; filename="{}.zip"'.format(
                    dirname
                )
            }
        )
        response.content_type = "application/zip"
        response.force_close()  # just set keep-alive to False
        await response.prepare(request)  # send headers
        zipper = Zipper(full_path)
        async with zipper:
            while True:
                await asyncio.sleep(0.01)
                chunk = await zipper.read()
                if chunk == b"":
                    # not necessary, called implicitly
                    # await response.write_eof()
                    logging.debug("Request succesfully processed...")
                    return response
                logging.debug("Sending archive chunk...")
                await response.write(chunk)
                logging.debug("Chunk sent...")
    raise web.HTTPNotFound(text="folder was deleted or never existed")


async def handle_index_page(request):
    async with aiofiles.open(
        os.path.join(settings.BASE_DIR, 'templates/index.html'), mode='r'
    ) as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


def get_app(storage):
    """prepare and return aiohttp app instance"""
    app = web.Application(middlewares=[web.normalize_path_middleware()])
    app["storage"] = storage
    app.add_routes([
        web.get("/", handle_index_page),
        web.get(r"/archive/{hash:[\d\w]{4,}}/", archivate),
    ])
    return app


def main():
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG)
    app = get_app(args.storage)
    web.run_app(app)


if __name__ == "__main__":
    main()
