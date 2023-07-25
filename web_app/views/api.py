import base64
import datetime
from uuid import uuid4

import aiofiles
from aiohttp.web import (
    Response, RouteTableDef,
    json_response, Request,
    HTTPNotFound, HTTPFound
)

from web_app.schemas import ImageSchema
from config.settings import settings, get_logger
from web_app.rabbit.publish import publish
from web_app.services import search_image_by_token, change_last_upload_time

logger = get_logger()

routes = RouteTableDef()


@routes.get('/')
async def hello(request):
    return Response(text="Hello, world")


@routes.get("/upload/{token}")
async def get_image(request: Request):
    token = request.match_info.get("token", "")
    get_token = await search_image_by_token(token)
    if get_token:
        return json_response(f"http://127.0.0.1:8081/media/{get_token.hex}")
        # raise HTTPFound(f'/media/{get_token.hex}')
    raise HTTPNotFound()


@routes.post("/upload")
async def upload_file(request: Request):
    data = await request.post()
    width = int(data.get("width", 300))
    height = int(data.get("height", 300))
    image = data.get("image")
    if image:
        token = uuid4()
        filename_extension = image.filename.split(".")[-1]
        img_content = image.file.read()
        image_base64 = base64.b64encode(img_content).decode('utf-8')
        logger.debug("pre calling publish")
        await publish(ImageSchema(
            width=width,
            height=height,
            uuid=token,
            extension_type=filename_extension,
            file=image_base64,
            upload_date=datetime.datetime.now()
        ).json())
        logger.debug(f"post called publish with token:{token.hex}")
        return json_response(dict(token=token.hex))
    return json_response(dict(data="not image"))


@routes.get("/media/{token}")
async def media(request: Request):
    token = request.match_info.get("token", "")
    await change_last_upload_time(token, datetime.datetime.now())

    async with aiofiles.open(settings.MEDIA_PATH / f"{token}-resized.jpeg", mode='rb') as handle:
        file = await handle.read()
        return Response(body=file, content_type="image/jpeg")
