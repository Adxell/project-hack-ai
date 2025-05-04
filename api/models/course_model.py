import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_name = Column(String(255), nullable=False)
    professor_id = Column(PGUUID(as_uuid=True), nullable=False)


class CourseStudens(Base):
    __tablename__ = 'course_students'
    course_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())