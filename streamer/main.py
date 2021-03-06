#!/usr/bin/env python3

import asyncio
import logging
import os

import aiofiles
from aiohttp import web
import dotenv

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
            break
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
    if not os.path.isdir(full_path):
        raise web.HTTPNotFound(text="folder was deleted or never existed")

    # ифчик инвертировал, но вообще пишу нормальный вариант
    # после ифа вполне осмысленно потому что есть вот такое мнение,
    # которое лично мне близко:
    #
    # Put the normal case after the if rather than after the else
    #
    # Put the case you normally expect to process first.
    # This is in line with the general principle of putting code
    # that results from a decision as close as possible to the decision.
    # (c) Code Complete, Steve McConnell

    response = get_archivate_response(dirname)
    await response.prepare(request)  # send headers
    async with Zipper(full_path) as zipper:
        await read_and_write_chunks(
            response, zipper, request.app["settings"].delay
        )
    return response


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
    dotenv.load_dotenv()
    args = get_args()
    logging.basicConfig(level=getattr(logging, args.log))
    app = get_app(args)
    web.run_app(app)


if __name__ == "__main__":
    main()
