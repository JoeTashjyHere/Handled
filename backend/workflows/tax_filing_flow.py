from typing import Any

from agents.tax_filing_eligibility import evaluate_tax_filing_eligibility
from models.task import Task
from workflows.engine import StepOutcome, WorkflowContext, WorkflowEngine, WorkflowStep


def _eligibility_step(context: WorkflowContext) -> StepOutcome:
    result = evaluate_tax_filing_eligibility(context.payload)
    return StepOutcome(
        success=result["eligible"],
        output=result,
        requires_human_review=result["requires_human_review"]
    )


def _collect_documents_step(context: WorkflowContext) -> StepOutcome:
    tax_year = context.payload.get("tax_year")
    checklist = [
        "Collect W-2/1099 forms",
        "Confirm filing status",
        "Verify state residency"
    ]
    return StepOutcome(success=True, output={"tax_year": tax_year, "checklist": checklist})


def run_tax_filing_flow(task: Task, payload: dict[str, Any], db) -> Task:
    steps = [
        WorkflowStep(name="eligibility_check", action=_eligibility_step, max_retries=1),
        WorkflowStep(name="collect_documents", action=_collect_documents_step, max_retries=0)
    ]
    engine = WorkflowEngine(steps)
    context = WorkflowContext(task=task, payload=payload, db=db)
    return engine.run(context)
