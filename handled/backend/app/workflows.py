from sqlalchemy.orm import Session

from .agents.eligibility import reimbursement_eligibility_stub
from .agents.intake import extract_receipt_fields_stub
from .models import Task, TaskStatus, TaskType


def initialize_steps(task: Task):
    if not task.steps:
        task.steps = {"timeline": [], "artifacts": {}, "notes": []}


def append_timeline(task: Task, event: str):
    task.steps.setdefault("timeline", [])
    task.steps["timeline"].append(event)


def run_workflow_tick(db: Session, task: Task):
    initialize_steps(task)

    if task.status == TaskStatus.intake:
        append_timeline(task, "Intake received. Planning next steps.")
        task.status = TaskStatus.planning

    elif task.status == TaskStatus.planning:
        if task.task_type == TaskType.reimbursement:
            append_timeline(task, "Preparing reimbursement packet.")
            task.status = TaskStatus.executing
        else:
            append_timeline(task, f"Planning workflow for {task.task_type}.")
            task.status = TaskStatus.executing

    elif task.status == TaskStatus.executing:
        if task.task_type == TaskType.reimbursement:
            files = getattr(task, "files", [])
            if files:
                extracted = extract_receipt_fields_stub(files[0].storage_path)
                elig = reimbursement_eligibility_stub(extracted)
                task.steps["artifacts"]["extracted"] = extracted
                task.steps["artifacts"]["eligibility"] = elig
                task.requires_human_review = bool(elig.get("human_review_required"))
                task.confidence_score = float(elig.get("confidence") or 0.0)

                if task.requires_human_review:
                    append_timeline(task, "Needs human review before submission.")
                    task.status = TaskStatus.needs_human_review
                else:
                    append_timeline(task, "Submitted reimbursement (stub).")
                    task.status = TaskStatus.waiting
            else:
                append_timeline(task, "Waiting for receipt uploads.")
                task.status = TaskStatus.waiting

        else:
            append_timeline(task, "Execution in progress (stub).")
            task.status = TaskStatus.needs_human_review

    elif task.status == TaskStatus.waiting:
        append_timeline(task, "Waiting on external response (stub).")

    db.add(task)
    db.commit()
    db.refresh(task)
