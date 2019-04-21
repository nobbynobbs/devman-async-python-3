#!/usr/bin/env python3


from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


def main():
    app = web.Application()
    app.add_routes([
        web.get("/", hello)
    ])
    web.run_app(app)


if __name__ == "__main__":
    main()
