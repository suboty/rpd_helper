from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.schemas import *
from app.services.documents import DocumentsService


DocumentsRouter = APIRouter(
    prefix="/v0/documents", tags=["documents"]
)


@DocumentsRouter.get("/", response_model=List[DocumentResponse])
async def index(
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    documents_service: DocumentsService = Depends(),
):
    return [
        document
        for document in await documents_service.list(
            page_size=page_size,
            start_index=start_index,
        )
    ]


@DocumentsRouter.get("/{document_id}", response_model=DocumentResponse)
async def get(document_id: int, documents_service: DocumentsService = Depends()):
    try:
        return await documents_service.get(document_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"Document with ID {document_id} is not found")


@DocumentsRouter.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    document: DocumentPayload,
    documents_service: DocumentsService = Depends(),
):
    return await documents_service.create(document)


@DocumentsRouter.patch("/{document_id}", response_model=DocumentResponse)
async def update(
    document_id: int,
    document: DocumentPayload,
    documents_service: DocumentsService = Depends(),
):
    return await documents_service.update(document_id, document)


@DocumentsRouter.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    document_id: int, documents_service: DocumentsService = Depends()
):
    return await documents_service.delete(document_id)
