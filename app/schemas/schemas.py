from app.schemas import *


class TextPayload(TextBase):
    pass


class TextResponse(TextBase):
    id: int
    updated_at: str


class CoursePayload(CourseBase):
    pass


class CourseResponse(CourseBase):
    id: int
    updated_at: str


class DocumentPayload(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    updated_at: str


class CompetencePayload(CompetenceBase):
    pass


class CompetenceResponse(CompetenceBase):
    id: int
    updated_at: str
