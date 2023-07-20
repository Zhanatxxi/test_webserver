from aiohttp import web


class WebApplication(web.Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
