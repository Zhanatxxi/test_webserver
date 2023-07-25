import datetime

import aiofiles
from aiohttp.web import (
    Response, RouteTableDef,
    Request, json_response
)
from aiohttp.web_exceptions import HTTPNotFound

from config.settings import settings
from web_app.services import change_last_upload_time, get_image_by_token

routes = RouteTableDef()


@routes.get("/media/{token}")
async def media(request: Request):
    token = request.match_info.get("token", "")
    image = await get_image_by_token(token)
    if not image:
        raise HTTPNotFound()
    await change_last_upload_time(token, datetime.datetime.now())

    async with aiofiles.open(settings.MEDIA_PATH / f"{token}-resized.{image.extension_type}", mode='rb') as handle:
        file = await handle.read()
        return Response(body=file, content_type="image/jpeg")


@routes.get("/")
async def test(request):
    return json_response("test")
