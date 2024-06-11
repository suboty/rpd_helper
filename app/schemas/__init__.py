from typing import Optional, Dict
from pydantic import BaseModel


class TextBase(BaseModel):
    document_id: int
    text: Optional[str]
    type: Optional[str]
    is_deleted: Optional[bool]

    class Config:
        orm_mode = True


class DocumentBase(BaseModel):
    courses_id: int
    type: str
    is_deleted: Optional[bool]

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    name: str
    params: Dict
    is_deleted: Optional[bool]

    class Config:
        orm_mode = True
