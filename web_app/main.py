from core import create_web_app
from web_app.views.api import routes as api_routes

api = create_web_app()
api.add_routes(api_routes)



