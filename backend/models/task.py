from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from models.database import Base


class TaskType(str, Enum):
    reimbursement = "reimbursement"
    scheduling = "scheduling"
    government_form = "government_form"
    tax_filing = "tax_filing"


class TaskStatus(str, Enum):
    intake = "intake"
    planning = "planning"
    executing = "executing"
    waiting = "waiting"
    completed = "completed"
    failed = "failed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    task_type = Column(String(32), nullable=False)
    status = Column(String(32), nullable=False, default=TaskStatus.intake.value)
    steps = Column(JSONB, nullable=False, default=list)
    confidence_score = Column(Float, nullable=True)
    requires_human_review = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
