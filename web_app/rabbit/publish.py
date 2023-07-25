import aio_pika

from config.settings import settings, get_logger


logger = get_logger()


async def publish(message) -> None:
    logger.debug("publish call")
    try:
        connection = await aio_pika.connect_robust(
            settings.MQ_PATH,
        )
    except Exception as e:
        logger.error(e)
        logger.error("publish error log")
    else:
        async with connection:
            routing_key = settings.ROUTING_KEY

            channel = await connection.channel()
            queue = await channel.declare_queue(routing_key)

            await channel.default_exchange.publish(
                aio_pika.Message(body=f"{message}".encode()),
                routing_key=queue.name,
            )
