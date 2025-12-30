from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db.session import get_db
from models.schemas import HealthResponse, IntakeRequest, ReviewDecision, TaskCreate, TaskResponse, TaskUpdate
from models.task import Task
from services.openai_client import summarize_intake
from workflows.tasks import enqueue_intake
from workflows.registry import get_workflow_runner

app = FastAPI(title="Handled API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/intake")
def create_intake(payload: IntakeRequest, db: Session = Depends(get_db)) -> dict:
    if not payload.summary:
        raise HTTPException(status_code=400, detail="Summary is required")

    ai_brief = summarize_intake(payload.summary)
    workflow_id = enqueue_intake(payload.summary, ai_brief)

    return {
        "workflow_id": workflow_id,
        "ai_brief": ai_brief
    }


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> Task:
    task = Task(
        user_id=payload.user_id,
        task_type=payload.task_type.value,
        status=payload.status.value,
        steps=payload.steps,
        confidence_score=payload.confidence_score,
        requires_human_review=payload.requires_human_review
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)) -> list[Task]:
    return db.query(Task).order_by(Task.created_at.desc()).all()


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = payload.model_dump(exclude_unset=True)
    if "task_type" in update_data:
        update_data["task_type"] = update_data["task_type"].value
    if "status" in update_data:
        update_data["status"] = update_data["status"].value

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None


@app.get("/review/tasks", response_model=list[TaskResponse])
def list_review_tasks(db: Session = Depends(get_db)) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.requires_human_review.is_(True))
        .order_by(Task.updated_at.desc())
        .all()
    )


@app.get("/review/tasks/{task_id}", response_model=TaskResponse)
def get_review_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/review/tasks/{task_id}/decision", response_model=TaskResponse)
def review_task(task_id: int, decision: ReviewDecision, db: Session = Depends(get_db)) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    review_step = {
        "name": "human_review",
        "action": decision.action,
        "reason": decision.reason,
        "payload": decision.payload,
        "timestamp": datetime.utcnow().isoformat()
    }

    steps = list(task.steps or [])
    steps.append(review_step)
    task.steps = steps

    if decision.action == "reject":
        task.status = "failed"
        task.requires_human_review = False
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    if decision.action == "edit":
        if decision.payload is None:
            raise HTTPException(status_code=400, detail="Payload is required for edits")
        task.requires_human_review = True
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    if decision.action == "approve":
        if decision.payload is None:
            raise HTTPException(status_code=400, detail="Payload is required for approval")
        task.requires_human_review = False
        db.add(task)
        db.commit()
        db.refresh(task)
        runner = get_workflow_runner(task.task_type)
        return runner(task, decision.payload, db)

    raise HTTPException(status_code=400, detail="Invalid review action")
