import docx
import regex
from fastapi import Depends

from app.services.competencies import CompetenciesService
from app.services.texts import TextsService
from app.services.documents import DocumentsService
from app.schemas.schemas import *


class DOCXParsingService:
    excluded_paragraphs = [
        ''
    ]

    excluded_paragraphs_re = [
        regex.compile(r'Время, отводимое на выполнение задания')
    ]

    competencies_re = {
        'Знать': regex.compile(r'УК\s?-\d.*Знать\s?-'),
        'Уметь': regex.compile(r'УК\s?-\d.*Уметь\s?-'),
        'Владеть': regex.compile(r'УК\s?-\d.*Владеть\s?-'),
    }

    def __init__(
            self,
            competencies_service: CompetenciesService = Depends(),
            texts_service: TextsService = Depends(),
            documents_service: DocumentsService = Depends(),
    ):
        self.current_document = None
        self.current_paragraphs = None
        self.current_document_id = None

        self.competencies_service = competencies_service
        self.texts_service = texts_service
        self.documents_service = documents_service

    def filter_paragraph(self, paragraph):

        if paragraph in self.excluded_paragraphs:
            return False
        for re in self.excluded_paragraphs_re:
            if re.match(paragraph):
                return False
        return True

    async def set_current_docx(self, course_id, type, path_to_file):
        self.current_document = self.load_document(path_to_file)
        doc_res = await self.documents_service.create(
            DocumentPayload(
                courses_id=course_id,
                type=type
            )
        )

        self.current_document_id = doc_res['id']

        _current_paragraphs = []
        _current_paragraph = []

        for paragraph in self.current_document.paragraphs:
            if paragraph.text != '':
                _current_paragraph.append(paragraph.text)
            else:
                _current_paragraphs.append(' '.join(_current_paragraph))
                _current_paragraph = []

        self.current_paragraphs = _current_paragraphs

    @staticmethod
    def load_document(path_to_file):
        return docx.Document(path_to_file)

    async def get_competencies(self):

        _current_comp_id = None

        competencies_counter = 0
        questions_number = 0

        for paragraph in self.current_paragraphs:
            if self.filter_paragraph(paragraph):
                for re_key in self.competencies_re.keys():
                    if self.competencies_re[re_key].findall(paragraph):
                        comp_res = await self.competencies_service.create(
                            CompetencePayload(
                                courses_id=1,
                                type=re_key,
                                competencies=[
                                    paragraph
                                ]
                            )
                        )
                        competencies_counter += 1
                        _current_comp_id = comp_res['id']
                if _current_comp_id:
                    await self.texts_service.create(
                        TextPayload(
                            document_id=self.current_document_id,
                            competencies_id=_current_comp_id,
                            text=paragraph,
                            type='question'
                        )
                    )
                    questions_number += 1
        return competencies_counter, questions_number
