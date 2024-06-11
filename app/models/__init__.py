from sqlalchemy.ext.declarative import declarative_base

from app.settings import settings

EntityMeta = declarative_base()


async def init():
    async with settings.get_setting('Engine').begin() as conn:
        await conn.run_sync(EntityMeta.metadata.create_all)
