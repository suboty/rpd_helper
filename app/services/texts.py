from typing import List, Optional

from fastapi import Depends
from app.models.models import Texts

from app.repositories.texts import TextsRepository
from app.schemas.schemas import TextPayload


class TextsService:
    texts_repository: TextsRepository

    def __init__(
            self, texts_repository: TextsRepository = Depends()
    ) -> None:
        self.texts_repository = texts_repository

    async def create(self, text_body: TextPayload) -> Texts:
        return await self.texts_repository.create(
            Texts(
                document_id=text_body.document_id,
                text=text_body.text,
                type=text_body.type,
            )
        )

    async def delete(self, text_id: int) -> None:
        return await self.texts_repository.delete(
            Texts(id=text_id)
        )

    async def get(self, text_id: int) -> Texts:
        return await self.texts_repository.get(
            Texts(id=text_id)
        )

    async def list(
            self,
            page_size: Optional[int] = 100,
            start_index: Optional[int] = 0,
    ) -> List[Texts]:
        return await self.texts_repository.list(
            limit=page_size,
            start=start_index,
        )

    async def update(
            self, text_id: int, text_body: TextPayload
    ) -> Texts:
        return await self.texts_repository.update(
            text_id, Texts(
                document_id=text_body.document_id,
                text=text_body.text,
                type=text_body.type,
            )
        )
