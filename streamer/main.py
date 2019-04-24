#!/usr/bin/env python3

import argparse
import logging
import os
import re

import aiofiles
from aiohttp import web

from streamer.zipper import Zipper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VALID_FOLDER_NAME = re.compile(r"^[\w\d]{4,}$")


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
    if not VALID_FOLDER_NAME.match(dirname):
        raise web.HTTPBadRequest(
            text="only letters and digits allowed in param"
        )

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
        await response.prepare(request)
        zipper = Zipper(full_path)
        async with zipper:
            while True:
                chunk = await zipper.read()
                if chunk == b"":
                    # not necessary, called implicitly
                    # await response.write_eof()
                    return response
                logging.debug("Sending archive chunk...")
                await response.write(chunk)
    raise web.HTTPNotFound(text="folder was deleted or never existed")


async def handle_index_page(request):
    async with aiofiles.open(
        os.path.join(BASE_DIR, 'templates/index.html'), mode='r'
    ) as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


def get_app(storage):
    """prepare and return aiohttp app instance"""
    app = web.Application(middlewares=[web.normalize_path_middleware()])
    app["storage"] = storage
    app.add_routes([
        web.get("/", handle_index_page),
        web.get("/archive/{hash}/", archivate),

    ])
    return app


def main():
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG)
    app = get_app(args.storage)
    web.run_app(app)


if __name__ == "__main__":
    main()
