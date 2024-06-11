from typing import List, Optional

from fastapi import Depends
from app.models.models import Documents

from app.repositories.documents import DocumentsRepository
from app.schemas.schemas import DocumentPayload


class DocumentsService:
    documents_repository: DocumentsRepository

    def __init__(
            self, documents_repository: DocumentsRepository = Depends()
    ) -> None:
        self.documents_repository = documents_repository

    async def create(self, document_body: DocumentPayload) -> Documents:
        return await self.documents_repository.create(
            Documents(
                courses_id=document_body.courses_id,
                type=document_body.type,
            )
        )

    async def delete(self, document_id: int) -> None:
        return await self.documents_repository.delete(
            Documents(id=document_id)
        )

    async def get(self, document_id: int) -> Documents:
        return await self.documents_repository.get(
            Documents(id=document_id)
        )

    async def list(
            self,
            page_size: Optional[int] = 100,
            start_index: Optional[int] = 0,
    ) -> List[Documents]:
        return await self.documents_repository.list(
            limit=page_size,
            start=start_index,
        )

    async def update(
            self, document_id: int, document_body: DocumentPayload
    ) -> Documents:
        return await self.documents_repository.update(
            document_id, Documents(
                courses_id=document_body.courses_id,
                type=document_body.type,
            )
        )
