from typing import Generator
import contextlib

from sqlalchemy.ext.asyncio import AsyncSession

from db.session import Session


@contextlib.asynccontextmanager
async def get_db_session() -> AsyncSession:
    async with Session() as session:
        yield session
