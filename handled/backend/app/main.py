import uuid

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, File, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .auth import (
    clear_session_cookie,
    get_current_user,
    get_or_create_user,
    make_magic_token,
    set_session_cookie,
    verify_magic_token,
)
from .config import settings
from .db import Base, engine, get_db
from .models import Task, TaskFile, TaskStatus, TaskType, User
from .schemas import MagicLinkRequest, MagicLinkVerify, TaskCreate, TaskOut, UserOut
from .storage import save_upload
from .workflows import append_timeline, initialize_steps, run_workflow_tick

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Handled API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.APP_BASE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/auth/request-magic-link")
def request_magic_link(payload: MagicLinkRequest):
    token = make_magic_token(payload.email)
    link = f"{settings.APP_BASE_URL}/login?token={token}"

    print(f"[DEV MAGIC LINK] {payload.email}: {link}")
    return {"sent": True}


@app.post("/auth/verify-magic-link")
def verify_link(payload: MagicLinkVerify, resp: Response, db: Session = Depends(get_db)):
    email = verify_magic_token(payload.token)
    user = get_or_create_user(db, email)
    set_session_cookie(resp, user.id)
    return {"ok": True}


@app.post("/auth/logout")
def logout(resp: Response):
    clear_session_cookie(resp)
    return {"ok": True}


@app.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return UserOut(id=user.id, email=user.email)


@app.post("/tasks", response_model=TaskOut)
def create_task(
    payload: TaskCreate,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = Task(
        id=str(uuid.uuid4()),
        user_id=user.id,
        task_type=payload.task_type,
        status=TaskStatus.intake,
        steps={"title": payload.title, "description": payload.description, "timeline": []},
        confidence_score=0.0,
        requires_human_review=False,
    )
    initialize_steps(task)
    append_timeline(task, "Task created.")
    db.add(task)
    db.commit()
    db.refresh(task)

    background.add_task(run_workflow_tick, db, task)

    return TaskOut(
        id=task.id,
        task_type=task.task_type,
        status=task.status,
        title=task.steps.get("title", ""),
        description=task.steps.get("description", ""),
        steps=task.steps,
        confidence_score=task.confidence_score,
        requires_human_review=task.requires_human_review,
    )


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        return Response(status_code=404)

    return TaskOut(
        id=task.id,
        task_type=task.task_type,
        status=task.status,
        title=task.steps.get("title", ""),
        description=task.steps.get("description", ""),
        steps=task.steps,
        confidence_score=task.confidence_score,
        requires_human_review=task.requires_human_review,
    )


@app.post("/tasks/{task_id}/upload")
def upload_task_file(
    task_id: str,
    file: UploadFile = File(...),
    background: BackgroundTasks = None,  # type: ignore
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        return Response(status_code=404)

    saved_name, path = save_upload(task_id, file)
    rec = TaskFile(
        id=str(uuid.uuid4()),
        task_id=task_id,
        filename=file.filename or saved_name,
        content_type=file.content_type or "application/octet-stream",
        storage_path=path,
    )
    db.add(rec)

    task.steps.setdefault("files", [])
    task.steps["files"].append({"filename": rec.filename, "content_type": rec.content_type})
    task.status = TaskStatus.planning
    append_timeline(task, f"File uploaded: {rec.filename}")

    db.add(task)
    db.commit()
    db.refresh(task)

    if background is not None:
        background.add_task(run_workflow_tick, db, task)
    else:
        run_workflow_tick(db, task)

    return {"ok": True, "filename": rec.filename}


@app.post("/tasks/{task_id}/tick")
def tick_task(task_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        return Response(status_code=404)
    run_workflow_tick(db, task)
    return {"ok": True, "status": task.status}
