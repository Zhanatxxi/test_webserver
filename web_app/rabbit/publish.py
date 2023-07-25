import aio_pika

from config.settings import settings


async def publish(message) -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    async with connection:
        routing_key = settings.ROUTING_KEY

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=f"{message}".encode()),
            routing_key=routing_key,
        )
