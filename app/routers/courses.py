from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.schemas import *
from app.services.courses import CoursesService


CoursesRouter = APIRouter(
    prefix="/courses", tags=["courses"]
)


@CoursesRouter.get("/", response_model=List[CourseResponse])
async def index(
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    courses_service: CoursesService = Depends(),
):
    return [
        course
        for course in await courses_service.list(
            page_size=page_size,
            start_index=start_index,
        )
    ]


@CoursesRouter.get("/{course_id}", response_model=CourseResponse)
async def get(course_id: int, courses_service: CoursesService = Depends()):
    try:
        return await courses_service.get(course_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Course with ID {course_id} is not found")


@CoursesRouter.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    course: CoursePayload,
    courses_service: CoursesService = Depends(),
):
    return await courses_service.create(course)


@CoursesRouter.patch("/{course_id}", response_model=CourseResponse)
async def update(
    course_id: int,
    course: CoursePayload,
    courses_service: CoursesService = Depends(),
):
    return await courses_service.update(course_id, course)


@CoursesRouter.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    course_id: int, courses_service: CoursesService = Depends()
):
    return await courses_service.delete(course_id)
