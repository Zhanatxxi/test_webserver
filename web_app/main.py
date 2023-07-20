from aiohttp import web

from core import create_web_app
from web_app.views.api import routes

app = create_web_app()
app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app)
