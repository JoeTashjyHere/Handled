from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from models.task import TaskStatus, TaskType


class HealthResponse(BaseModel):
    status: str


class IntakeRequest(BaseModel):
    summary: str = Field(..., min_length=5, description="Short description of the life admin request")


class TaskBase(BaseModel):
    user_id: int
    task_type: TaskType
    status: TaskStatus = TaskStatus.intake
    steps: list[dict[str, Any]] = Field(default_factory=list)
    confidence_score: float | None = None
    requires_human_review: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    task_type: TaskType | None = None
    status: TaskStatus | None = None
    steps: list[dict[str, Any]] | None = None
    confidence_score: float | None = None
    requires_human_review: bool | None = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ReviewDecision(BaseModel):
    action: str = Field(..., pattern="^(approve|edit|reject)$")
    payload: dict[str, Any] | None = None
    reason: str | None = None
