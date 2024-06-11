from typing import List, Optional

from fastapi import Depends
from app.models.models import Courses

from app.repositories.courses import CoursesRepository
from app.schemas.schemas import CoursePayload


class CoursesService:
    courses_repository: CoursesRepository

    def __init__(
            self, courses_repository: CoursesRepository = Depends()
    ) -> None:
        self.courses_repository = courses_repository

    async def create(self, course_body: CoursePayload) -> Courses:
        return await self.courses_repository.create(
            Courses(
                name=course_body.name,
                params=course_body.params,
            )
        )

    async def delete(self, course_id: int) -> None:
        return await self.courses_repository.delete(
            Courses(id=course_id)
        )

    async def get(self, course_id: int) -> Courses:
        return await self.courses_repository.get(
            Courses(id=course_id)
        )

    async def list(
            self,
            page_size: Optional[int] = 100,
            start_index: Optional[int] = 0,
    ) -> List[Courses]:
        return await self.courses_repository.list(
            limit=page_size,
            start=start_index,
        )

    async def update(
            self, course_id: int, course_body: CoursePayload
    ) -> Courses:
        return await self.courses_repository.update(
            course_id, Courses(
                name=course_body.name,
                params=course_body.params,
            )
        )
