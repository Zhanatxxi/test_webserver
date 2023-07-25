import datetime

import aiofiles
from aiohttp.web import (
    Response, RouteTableDef,
    Request, json_response
)

from config.settings import settings
from web_app.services import search_image_by_token, change_last_upload_time

routes = RouteTableDef()


@routes.get("/media/{token}")
async def media(request: Request):
    token = request.match_info.get("token", "")
    await change_last_upload_time(token, datetime.datetime.now())

    async with aiofiles.open(settings.MEDIA_PATH / f"{token}-resized.jpeg", mode='rb') as handle:
        file = await handle.read()
        return Response(body=file, content_type="image/jpeg")


@routes.get("/")
async def test(request):
    return json_response("test")
