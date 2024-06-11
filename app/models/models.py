from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import JSONB, TEXT
from sqlalchemy.sql import func

from app.models import EntityMeta


class Texts(EntityMeta):
    __tablename__ = 'texts'

    id = Column(BigInteger, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    document_id = Column(Integer, ForeignKey('documents.id'), index=True, nullable=False)
    text = Column(TEXT, nullable=True)
    type = Column(String, nullable=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    def normalize(self):
        return {
            "id": self.id,
            "document_id": self.document_id,
            "text": self.text.__str__(),
            "type": self.type.__str__(),
            "updated_at": self.updated_at.__str__(),
        }


class Documents(EntityMeta):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    courses_id = Column(Integer, ForeignKey('courses.id'), index=True, nullable=False)
    type = Column(String, nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    def normalize(self):
        return {
            "id": self.id,
            "courses_id": self.courses_id,
            "type": self.type.__str__(),
            "updated_at": self.updated_at.__str__(),
        }


class Courses(EntityMeta):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    params = Column(JSONB, nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    def normalize(self):
        return {
            "id": self.id,
            "name": self.name.__str__(),
            "params": self.type,
            "updated_at": self.updated_at.__str__(),
        }


class Competencies(EntityMeta):
    __tablename__ = 'competencies'

    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False, autoincrement=True)
    courses_id = Column(Integer, ForeignKey('courses.id'), index=True, nullable=False)
    competencies = Column(ARRAY(String), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    def normalize(self):
        return {
            "id": self.id,
            "courses_id": self.courses_id,
            "competencies": self.competencies,
            "updated_at": self.updated_at.__str__(),
        }
