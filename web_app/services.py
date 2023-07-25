import io
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from PIL import Image as pilImage

from config.settings import settings
from db.deps import get_db_session
from web_app.models import Image


async def save_image(
    uuid,
    upload_date,
    extension_type
):
    async with get_db_session() as session:
        image = Image(
            uuid=uuid,
            upload_date=upload_date,
            extension_type=extension_type
        )
        session.add(image)
        await session.commit()


async def search_image_by_token(
    token
) -> UUID:
    async with get_db_session() as session:
        stmt = select(Image.uuid).where(Image.uuid == token)
        token = await session.scalar(stmt)
        return token


async def get_image_by_token(
    token: str
) -> Image:
    async with get_db_session() as session:
        stmt = select(Image).where(Image.uuid == token)
        image = await session.scalar(stmt)
        return image


async def set_finished_date(
    token,
    date
):
    async with get_db_session() as session:
        image = await session.scalar(
            select(
                Image
            ).where(Image.uuid == token)
        )
        image.finished_date = date
        await session.commit()


async def change_last_upload_time(
    token,
    date
):
    async with get_db_session() as session:
        image = await session.scalar(
            select(
                Image
            ).where(Image.uuid == token)
        )
        image.last_upload_date = date
        await session.commit()


def get_full_name(token, extension_type, resized=False):
    return "{}-resized.{}".format(token, extension_type) \
        if resized else "{}.{}".format(token, extension_type)


async def save_images(
    token: str,
    extension_type: str,
    image,
    width: int,
    height: int
):
    img = pilImage.open(io.BytesIO(image))
    img.save(settings.MEDIA_PATH / get_full_name(token, extension_type))

    new_image = img.resize((width, height))
    new_image.save(settings.MEDIA_PATH / get_full_name(token, extension_type, resized=True))
    await set_finished_date(token, datetime.now())
