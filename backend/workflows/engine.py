from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from sqlalchemy.orm import Session

from models.task import Task, TaskStatus


@dataclass
class WorkflowContext:
    task: Task
    payload: dict[str, Any]
    db: Session


@dataclass
class StepOutcome:
    success: bool
    output: dict[str, Any]
    requires_human_review: bool = False


@dataclass
class WorkflowStep:
    name: str
    action: Callable[[WorkflowContext], StepOutcome]
    max_retries: int = 2


class WorkflowEngine:
    def __init__(self, steps: list[WorkflowStep]) -> None:
        self.steps = steps

    def run(self, context: WorkflowContext) -> Task:
        self._update_task_status(context.task, context.db, TaskStatus.executing.value)
        self._update_review_flag(context.task, context.db, False)

        for step in self.steps:
            outcome = self._run_step(context, step)
            if outcome.requires_human_review:
                self._update_task_status(context.task, context.db, TaskStatus.waiting.value)
                self._update_review_flag(context.task, context.db, True)
                return context.task
            if not outcome.success:
                self._update_task_status(context.task, context.db, TaskStatus.failed.value)
                return context.task

        self._update_task_status(context.task, context.db, TaskStatus.completed.value)
        self._update_review_flag(context.task, context.db, False)
        return context.task

    def _run_step(self, context: WorkflowContext, step: WorkflowStep) -> StepOutcome:
        attempt = 0
        last_error: str | None = None

        while attempt <= step.max_retries:
            attempt += 1
            try:
                outcome = step.action(context)
                step_state = {
                    "name": step.name,
                    "attempt": attempt,
                    "success": outcome.success,
                    "requires_human_review": outcome.requires_human_review,
                    "output": outcome.output,
                    "timestamp": datetime.utcnow().isoformat()
                }
                self._persist_step(context.task, context.db, step_state)
                return outcome
            except Exception as exc:  # noqa: BLE001 - workflow should capture failures
                last_error = str(exc)
                step_state = {
                    "name": step.name,
                    "attempt": attempt,
                    "success": False,
                    "requires_human_review": False,
                    "output": {"error": last_error},
                    "timestamp": datetime.utcnow().isoformat()
                }
                self._persist_step(context.task, context.db, step_state)
                if attempt > step.max_retries:
                    return StepOutcome(success=False, output={"error": last_error})

        return StepOutcome(success=False, output={"error": last_error or "Unknown error"})

    @staticmethod
    def _persist_step(task: Task, db: Session, step_state: dict[str, Any]) -> None:
        steps = list(task.steps or [])
        steps.append(step_state)
        task.steps = steps
        db.add(task)
        db.commit()
        db.refresh(task)

    @staticmethod
    def _update_task_status(task: Task, db: Session, status: str) -> None:
        task.status = status
        db.add(task)
        db.commit()
        db.refresh(task)

    @staticmethod
    def _update_review_flag(task: Task, db: Session, requires_review: bool) -> None:
        task.requires_human_review = requires_review
        db.add(task)
        db.commit()
        db.refresh(task)
