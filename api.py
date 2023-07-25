from aiohttp import web

from web_app import main


if __name__ == '__main__':
    web.run_app(main.api)
