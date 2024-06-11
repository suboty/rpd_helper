from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.schemas import *
from app.services.texts import TextsService


TextsRouter = APIRouter(
    prefix="/v0/texts", tags=["texts"]
)


@TextsRouter.get("/", response_model=List[TextResponse])
async def index(
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    texts_service: TextsService = Depends(),
):
    return [
        text
        for text in await texts_service.list(
            page_size=page_size,
            start_index=start_index,
        )
    ]


@TextsRouter.get("/{text_id}", response_model=TextResponse)
async def get(text_id: int, texts_service: TextsService = Depends()):
    try:
        return await texts_service.get(text_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Text with ID {text_id} is not found")


@TextsRouter.post(
    "/",
    response_model=TextResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    text: TextPayload,
    texts_service: TextsService = Depends(),
):
    return await texts_service.create(text)


@TextsRouter.patch("/{text_id}", response_model=TextResponse)
async def update(
    text_id: int,
    text: TextPayload,
    texts_service: TextsService = Depends(),
):
    return await texts_service.update(text_id, text)


@TextsRouter.delete(
    "/{text_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    text_id: int, texts_service: TextsService = Depends()
):
    return await texts_service.delete(text_id)
