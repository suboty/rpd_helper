from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.logger import logger
from app.connect_to_db import get_db_connection
from app.models.models import Texts
from app.repositories import decorator_rollback_error


class TextsRepository:
    db: AsyncSession

    def __init__(
            self, db: AsyncSession = Depends(get_db_connection)
    ) -> None:
        self.db = db

    @decorator_rollback_error
    async def list(
            self,
            limit: Optional[int],
            start: Optional[int],
    ) -> List[Texts]:
        res = await self.db.execute(select(Texts).order_by(desc(Texts.updated_at)).offset(start).limit(limit))
        logger.debug(f'Get Texts from <{start}> to <{limit}>')
        return [dict(x)['Texts'].normalize() for x in res.mappings().all()]

    @decorator_rollback_error
    async def get(self, text: Texts) -> Texts:
        res = await self.db.get(
            Texts,
            text.id,
        )
        logger.debug(f'Get Text with ID <{res.id}>')
        return res.normalize()

    @decorator_rollback_error
    async def create(self, text: Texts) -> Texts:
        self.db.add(text)
        await self.db.commit()
        await self.db.refresh(text)
        logger.debug(f'Create Text with type <{text.type}>')
        return text.normalize()

    @decorator_rollback_error
    async def update(self, _id: int, text: Texts) -> Texts:
        text.id = _id
        await self.db.merge(text)
        await self.db.commit()
        logger.debug(f'Update Text with ID <{_id}>')
        return text.normalize()

    @decorator_rollback_error
    async def delete(self, text: Texts) -> None:
        row = await self.db.execute(select(Texts).where(Texts.id == text.id))
        await self.db.delete(row.scalar_one())
        await self.db.commit()
        await self.db.flush()
        logger.debug(f'Delete Text with ID <{text.id}>')
