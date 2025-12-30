from typing import Any

from agents.scheduling_eligibility import evaluate_scheduling_eligibility
from models.task import Task
from workflows.engine import StepOutcome, WorkflowContext, WorkflowEngine, WorkflowStep


def _eligibility_step(context: WorkflowContext) -> StepOutcome:
    result = evaluate_scheduling_eligibility(context.payload)
    return StepOutcome(
        success=result["eligible"],
        output=result,
        requires_human_review=result["requires_human_review"]
    )


def _propose_times_step(context: WorkflowContext) -> StepOutcome:
    window = context.payload.get("availability_window", "")
    participants = context.payload.get("participants", [])
    suggestion = {
        "summary": "Propose times based on availability window.",
        "availability_window": window,
        "participants": participants
    }
    return StepOutcome(success=True, output=suggestion)


def run_scheduling_flow(task: Task, payload: dict[str, Any], db) -> Task:
    steps = [
        WorkflowStep(name="eligibility_check", action=_eligibility_step, max_retries=1),
        WorkflowStep(name="propose_times", action=_propose_times_step, max_retries=0)
    ]
    engine = WorkflowEngine(steps)
    context = WorkflowContext(task=task, payload=payload, db=db)
    return engine.run(context)
