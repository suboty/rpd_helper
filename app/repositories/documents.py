from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.logger import logger
from app.connect_to_db import get_db_connection
from app.models.models import Documents
from app.repositories import decorator_rollback_error


class DocumentsRepository:
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
    ) -> List[Documents]:
        res = await self.db.execute(select(Documents).order_by(desc(Documents.updated_at)).offset(start).limit(limit))
        logger.debug(f'Get Documents from <{start}> to <{limit}>')
        return [dict(x)['Documents'].normalize() for x in res.mappings().all()]

    @decorator_rollback_error
    async def get(self, document: Documents) -> Documents:
        res = await self.db.get(
            Documents,
            document.id,
        )
        logger.debug(f'Get Document with ID <{res.id}>')
        return res.normalize()

    @decorator_rollback_error
    async def create(self, document: Documents) -> Documents:
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        logger.debug(f'Create Document with name <{document.name}>')
        return document.normalize()

    @decorator_rollback_error
    async def update(self, _id: int, document: Documents) -> Documents:
        document.id = _id
        await self.db.merge(document)
        await self.db.commit()
        logger.debug(f'Update Document with ID <{_id}>')
        return document.normalize()

    @decorator_rollback_error
    async def delete(self, document: Documents) -> None:
        row = await self.db.execute(select(Documents).where(Documents.id == document.id))
        await self.db.delete(row.scalar_one())
        await self.db.commit()
        await self.db.flush()
        logger.debug(f'Delete Document with ID <{document.id}>')
