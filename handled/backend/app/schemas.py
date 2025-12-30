from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field

from .models import TaskStatus, TaskType


class MagicLinkRequest(BaseModel):
    email: EmailStr


class MagicLinkVerify(BaseModel):
    token: str


class UserOut(BaseModel):
    id: str
    email: EmailStr


class TaskCreate(BaseModel):
    task_type: TaskType
    title: str = Field(min_length=2, max_length=120)
    description: str = Field(default="", max_length=4000)


class TaskOut(BaseModel):
    id: str
    task_type: TaskType
    status: TaskStatus
    title: str
    description: str
    steps: dict[str, Any]
    confidence_score: float
    requires_human_review: bool

    class Config:
        from_attributes = True


class TaskUpdateStatus(BaseModel):
    status: TaskStatus
    steps: Optional[dict[str, Any]] = None
    confidence_score: Optional[float] = None
    requires_human_review: Optional[bool] = None
