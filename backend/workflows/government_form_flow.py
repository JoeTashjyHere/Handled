from typing import Any

from agents.government_form_eligibility import evaluate_government_form_eligibility
from models.task import Task
from workflows.engine import StepOutcome, WorkflowContext, WorkflowEngine, WorkflowStep


def _eligibility_step(context: WorkflowContext) -> StepOutcome:
    result = evaluate_government_form_eligibility(context.payload)
    return StepOutcome(
        success=result["eligible"],
        output=result,
        requires_human_review=result["requires_human_review"]
    )


def _collect_requirements_step(context: WorkflowContext) -> StepOutcome:
    form_type = context.payload.get("form_type", "")
    jurisdiction = context.payload.get("jurisdiction", "")
    checklist = [
        "Verify applicant identity documents",
        "Collect required supporting documentation",
        "Confirm submission method for jurisdiction"
    ]
    return StepOutcome(
        success=True,
        output={
            "form_type": form_type,
            "jurisdiction": jurisdiction,
            "checklist": checklist
        }
    )


def run_government_form_flow(task: Task, payload: dict[str, Any], db) -> Task:
    steps = [
        WorkflowStep(name="eligibility_check", action=_eligibility_step, max_retries=1),
        WorkflowStep(name="collect_requirements", action=_collect_requirements_step, max_retries=0)
    ]
    engine = WorkflowEngine(steps)
    context = WorkflowContext(task=task, payload=payload, db=db)
    return engine.run(context)
