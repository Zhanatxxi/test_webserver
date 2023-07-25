import asyncio
from time import sleep

from web_app.rabbit.consumer import consume


if __name__ == '__main__':
    sleep(8)
    asyncio.run(consume())
