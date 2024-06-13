from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.logger import logger
from app.connect_to_db import get_db_connection
from app.models.models import Competencies
from app.repositories import decorator_rollback_error


class CompetenciesRepository:
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
    ) -> List[Competencies]:
        res = await self.db.execute(select(Competencies)
                                    .order_by(desc(Competencies.updated_at))
                                    .offset(start).limit(limit))
        logger.debug(f'Get Competencies from <{start}> to <{limit}>')
        return [dict(x)['Competencies'].normalize() for x in res.mappings().all()]

    @decorator_rollback_error
    async def get(self, competence: Competencies) -> Competencies:
        res = await self.db.get(
            Competencies,
            competence.id,
        )
        logger.debug(f'Get Competence with ID <{res.id}>')
        return res.normalize()

    @decorator_rollback_error
    async def create(self, competence: Competencies) -> Competencies:
        self.db.add(competence)
        await self.db.commit()
        await self.db.refresh(competence)
        logger.debug(f'Create Competence with competencies <{competence.competencies}>')
        return competence.normalize()

    @decorator_rollback_error
    async def update(self, _id: int, competence: Competencies) -> Competencies:
        competence.id = _id
        await self.db.merge(competence)
        await self.db.commit()
        logger.debug(f'Update Competence with ID <{_id}>')
        return competence.normalize()

    @decorator_rollback_error
    async def delete(self, competence: Competencies) -> None:
        row = await self.db.execute(select(Competencies).where(Competencies.id == competence.id))
        await self.db.delete(row.scalar_one())
        await self.db.commit()
        await self.db.flush()
        logger.debug(f'Delete Competence with ID <{competence.id}>')
