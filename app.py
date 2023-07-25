from aiohttp import web

from core import create_web_app
from web_app.views.app import routes as app_routes


app = create_web_app()
app.add_routes(app_routes)


if __name__ == '__main__':
    web.run_app(app, port=8081)
