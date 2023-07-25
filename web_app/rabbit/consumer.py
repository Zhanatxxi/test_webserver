import asyncio
import base64
import io
import json

import aio_pika
from PIL import Image

from config.settings import settings
from web_app.schemas import ImageSchema
from web_app.services import save_image, save_images


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        image = ImageSchema(**json.loads(message.body))
        file = base64.b64decode(image.file)

        await save_image(image.uuid.hex, image.upload_date)
        await save_images(image.uuid.hex, image.extension_type, file, image.width, image.height)


async def main() -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    queue_name = settings.ROUTING_KEY

    channel = await connection.channel()

    await channel.set_qos(prefetch_count=settings.PREFETCH_COUNT)

    queue = await channel.declare_queue(queue_name)

    await queue.consume(process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()
