import asyncio

from web_app.rabbit.consumer import consume


if __name__ == '__main__':
    asyncio.run(consume())
