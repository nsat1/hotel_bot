from db import base  # noqa
from db.base_class import Base
from db.session import engine

import models, repo  # noqa


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
