from typing import Optional, Dict, List
from pydantic import BaseModel


class TextBase(BaseModel):
    document_id: int
    text: Optional[str]
    type: Optional[str]

    class Config:
        orm_mode = True


class DocumentBase(BaseModel):
    courses_id: int
    type: str

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str
    params: Dict

    class Config:
        orm_mode = True


class CompetenceBase(BaseModel):
    courses_id: int
    competencies: List[str]

    class Config:
        orm_mode = True