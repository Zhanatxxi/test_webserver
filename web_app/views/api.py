import base64
import datetime
import io
from uuid import uuid4

import aiofiles
from PIL import Image
from aiohttp.web import (
    Response, RouteTableDef,
    json_response, Request,
    HTTPNotFound, HTTPFound
)

from web_app.schemas import ImageSchema
from config.settings import settings
from web_app.rabbit.publish import publish
from web_app.services import save_image, search_image_by_token, change_last_upload_time

routes = RouteTableDef()


@routes.get('/')
async def hello(request):
    return Response(text="Hello, world")


@routes.get("/data")
async def json_response_answer(request: Request):
    return json_response({"data": "hi"})


@routes.post("/data")
async def get_data(request: Request):
    data = await request.json()
    return json_response(dict(data=data["data"]))


@routes.get("/upload/{token}")
async def get_image(request: Request):
    token = request.match_info.get("token", "")
    get_token = await search_image_by_token(token)
    if get_token:
        # return json_response(f"http://localhost:8080/media/{get_token.hex}")
        raise HTTPFound(f'/media/{get_token.hex}')
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
        await publish(ImageSchema(
            width=width,
            height=height,
            uuid=token,
            extension_type=filename_extension,
            file=image_base64,
            upload_date=datetime.datetime.now()
        ).json())
        return json_response(dict(token=token.hex))
    return json_response(dict(data="not image"))


@routes.get("/media/{token}")
async def media(request: Request):
    token = request.match_info.get("token", "")
    await change_last_upload_time(token, datetime.datetime.now())

    async with aiofiles.open(settings.MEDIA_PATH / f"{token}-resized.jpeg", mode='rb') as handle:
        file = await handle.read()
        return Response(body=file, content_type="image/jpeg")
