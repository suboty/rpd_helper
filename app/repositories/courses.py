from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.logger import logger
from app.connect_to_db import get_db_connection
from app.models.models import Courses
from app.repositories import decorator_rollback_error


class CoursesRepository:
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
    ) -> List[Courses]:
        res = await self.db.execute(select(Courses).order_by(desc(Courses.updated_at)).offset(start).limit(limit))
        logger.debug(f'Get Courses from <{start}> to <{limit}>')
        return [dict(x)['Courses'].normalize() for x in res.mappings().all()]

    @decorator_rollback_error
    async def get(self, course: Courses) -> Courses:
        res = await self.db.get(
            Courses,
            course.id,
        )
        logger.debug(f'Get Course with ID <{res.id}>')
        return res.normalize()

    @decorator_rollback_error
    async def create(self, course: Courses) -> Courses:
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        logger.debug(f'Create Course with name <{course.name}>')
        return course.normalize()

    @decorator_rollback_error
    async def update(self, _id: int, course: Courses) -> Courses:
        course.id = _id
        await self.db.merge(course)
        await self.db.commit()
        logger.debug(f'Update Course with ID <{_id}>')
        return course.normalize()

    @decorator_rollback_error
    async def delete(self, course: Courses) -> None:
        row = await self.db.execute(select(Courses).where(Courses.id == course.id))
        await self.db.delete(row.scalar_one())
        await self.db.commit()
        await self.db.flush()
        logger.debug(f'Delete Course with ID <{course.id}>')
