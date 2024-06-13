import os

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.settings import settings

metadata_obj = MetaData(schema=os.environ.get('DATABASE_SCHEMA'))


class EntityMeta(DeclarativeBase):
    metadata = metadata_obj
    schema = os.environ.get('DATABASE_SCHEMA')


async def init():
    async with settings.get_setting('Engine').begin() as conn:
        await conn.run_sync(EntityMeta.metadata.create_all)
