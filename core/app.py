from .base import WebApplication


def create_web_app():
    """ function return instance aiohttp.web.Application """
    return WebApplication(client_max_size=1024**3)
