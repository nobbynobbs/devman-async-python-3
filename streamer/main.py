#!/usr/bin/env python3

import asyncio
import logging
import os

import aiofiles
from aiohttp import web

from streamer.zipper import Zipper
import streamer.settings as settings
from streamer.settings import get_args


async def read_and_write_chunks(response, reader, delay):
    while True:
        await asyncio.sleep(delay)
        chunk = await reader.read()
        if chunk == b"":
            # not necessary, called implicitly
            # await response.write_eof()
            logging.debug("Request succesfully processed...")
            return response
        logging.debug("Sending archive chunk...")
        await response.write(chunk)
        logging.debug("Chunk sent...")


def get_archivate_response(dirname):
    response = web.StreamResponse(
        headers={
            "Content-Disposition": 'attachment; filename="{}.zip"'.format(
                dirname
            )
        }
    )
    response.content_type = "application/zip"
    response.force_close()  # just set keep-alive to False
    return response


async def archivate(request):
    logging.debug("Accepting request...")
    dirname = request.match_info["hash"]  # type: str
    base_path = request.app["settings"].storage
    full_path = os.path.join(base_path, dirname)
    if os.path.isdir(full_path):
        response = get_archivate_response(dirname)
        await response.prepare(request)  # send headers
        zipper = Zipper(full_path)
        async with zipper:
            result = await read_and_write_chunks(
                response, zipper, request.app["settings"].delay
            )
        return result
    raise web.HTTPNotFound(text="folder was deleted or never existed")


async def handle_index_page(request):
    async with aiofiles.open(
        os.path.join(settings.BASE_DIR, 'templates/index.html'), mode='r'
    ) as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


def get_app(args):
    """prepare and return aiohttp app instance"""
    app = web.Application(middlewares=[web.normalize_path_middleware()])
    app["settings"] = args
    app.add_routes([
        web.get("/", handle_index_page),
        web.get(r"/archive/{hash:[\d\w]{4,}}/", archivate),
    ])
    return app


def main():
    args = get_args()
    logging.basicConfig(level=getattr(logging, args.log))
    app = get_app(args)
    web.run_app(app)


if __name__ == "__main__":
    main()
