import aiofiles

import docx
from fastapi import APIRouter, Depends, UploadFile, status, HTTPException

from app.schemas.schemas import *
from app.services.docx_parsing import DOCXParsingService
from app.services.pptx_parsing import PPTXParsingService
from app.logger import logger


InterfaceRouter = APIRouter(
    prefix="/interface", tags=["interface"]
)


@InterfaceRouter.post(
    "/add_af",
    response_model=InterfaceAFResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
        course_id: str,
        af_file: UploadFile,
        docx_parsing_service: DOCXParsingService = Depends(),
):

    async with aiofiles.open('af.docx', 'wb') as out_file:
        content = await af_file.read()
        await out_file.write(content)

    await docx_parsing_service.set_current_docx(
        course_id=course_id,
        type='ФОС',
        path_to_file='af.docx'
    )
    comp_n, ques_n = await docx_parsing_service.get_competencies()

    return InterfaceAFResponse(
        status=True,
        message=f'Find {comp_n} competencies and {ques_n} questions'
    )

@InterfaceRouter.post(
    "/add_lecture",
    response_model=InterfaceLectureResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
        course_id: str,
        lecture_file: UploadFile,
        pptx_parsing_service: PPTXParsingService = Depends(),
):

    async with aiofiles.open('lecture.pptx', 'wb') as out_file:
        content = await lecture_file.read()
        await out_file.write(content)

    await pptx_parsing_service.set_current_docx(
        course_id=course_id,
        type='Лекция',
        path_to_file='lecture.pptx'
    )
    text_n = await pptx_parsing_service.get_lecture_text()

    return InterfaceAFResponse(
        status=True,
        message=f'Find {text_n} texts'
    )
