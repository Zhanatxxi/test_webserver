from .base import WebApplication


def create_web_app():
    """ function return instance aiohttp.web.Application """
    return WebApplication()
