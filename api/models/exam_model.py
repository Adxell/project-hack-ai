import uuid
from sqlalchemy import Column, String, ForeignKey, Table, DateTime, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList

Base = declarative_base()

class Exam(Base):
    __tablename__ = 'exams'
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(String(255), nullable=False)
    questions = Column(MutableList.as_mutable(JSON), nullable=False)
    professor_id = Column(PGUUID(as_uuid=True), nullable=False)


class ExamResult(Base):
    __tablename__ = 'exam_results'
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_id = Column(PGUUID(as_uuid=True), ForeignKey('exams.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(PGUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    score = Column(Numeric(5,2), nullable=False)
    answers = Column(JSON)
    taken_at = Column(DateTime(timezone=True), server_default=func.now())