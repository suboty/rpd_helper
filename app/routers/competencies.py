from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.schemas import *
from app.services.competencies import CompetenciesService


CompetenciesRouter = APIRouter(
    prefix="/competencies", tags=["competencies"]
)


@CompetenciesRouter.get("/", response_model=List[CompetenceResponse])
async def index(
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    competencies_service: CompetenciesService = Depends(),
):
    return [
        competence
        for competence in await competencies_service.list(
            page_size=page_size,
            start_index=start_index,
        )
    ]


@CompetenciesRouter.get("/{competence_id}", response_model=CompetenceResponse)
async def get(competence_id: int, competencies_service: CompetenciesService = Depends()):
    try:
        return await competencies_service.get(competence_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Competence with ID {competence_id} is not found")


@CompetenciesRouter.post(
    "/",
    response_model=CompetenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    competence: CompetencePayload,
    competencies_service: CompetenciesService = Depends(),
):
    return await competencies_service.create(competence)


@CompetenciesRouter.patch("/{competence_id}", response_model=CompetenceResponse)
async def update(
    competence_id: int,
    competence: CompetencePayload,
    competencies_service: CompetenciesService = Depends(),
):
    return await competencies_service.update(competence_id, competence)


@CompetenciesRouter.delete(
    "/{competence_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    competence_id: int, competencies_service: CompetenciesService = Depends()
):
    return await competencies_service.delete(competence_id)
