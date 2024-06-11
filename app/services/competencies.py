from typing import List, Optional

from fastapi import Depends
from app.models.models import Competencies

from app.repositories.competencies import CompetenciesRepository
from app.schemas.schemas import CompetencePayload


class CompetenciesService:
    competencies_repository: CompetenciesRepository

    def __init__(
            self, competencies_repository: CompetenciesRepository = Depends()
    ) -> None:
        self.competencies_repository = competencies_repository

    async def create(self, competence_body: CompetencePayload) -> Competencies:
        return await self.competencies_repository.create(
            Competencies(
                courses_id=competence_body.courses_id,
                competencies=competence_body.competencies,
            )
        )

    async def delete(self, competence_id: int) -> None:
        return await self.competencies_repository.delete(
            Competencies(id=competence_id)
        )

    async def get(self, competence_id: int) -> Competencies:
        return await self.competencies_repository.get(
            Competencies(id=competence_id)
        )

    async def list(
            self,
            page_size: Optional[int] = 100,
            start_index: Optional[int] = 0,
    ) -> List[Competencies]:
        return await self.competencies_repository.list(
            limit=page_size,
            start=start_index,
        )

    async def update(
            self, competence_id: int, competence_body: CompetencePayload
    ) -> Competencies:
        return await self.competencies_repository.update(
            competence_id, Competencies(
                courses_id=competence_body.courses_id,
                competencies=competence_body.competencies,
            )
        )
