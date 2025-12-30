import os
import uuid

from fastapi import UploadFile

from .config import settings


def ensure_upload_dir():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


def save_upload(task_id: str, file: UploadFile) -> tuple[str, str]:
    ensure_upload_dir()
    ext = os.path.splitext(file.filename or "")[1]
    safe_name = f"{uuid.uuid4().hex}{ext}"
    task_dir = os.path.join(settings.UPLOAD_DIR, task_id)
    os.makedirs(task_dir, exist_ok=True)
    path = os.path.join(task_dir, safe_name)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return safe_name, path
