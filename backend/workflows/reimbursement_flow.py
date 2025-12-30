from typing import Any

from agents.hsa_fsa_eligibility import evaluate_hsa_fsa_eligibility
from models.task import Task
from workflows.engine import StepOutcome, WorkflowContext, WorkflowEngine, WorkflowStep


def _eligibility_step(context: WorkflowContext) -> StepOutcome:
    result = evaluate_hsa_fsa_eligibility(context.payload)
    return StepOutcome(
        success=result["eligible"],
        output=result,
        requires_human_review=result["requires_human_review"]
    )


def _plan_step(context: WorkflowContext) -> StepOutcome:
    summary = context.payload.get("summary", "Reimbursement request")
    plan = [
        "Collect receipt and supporting documentation",
        "Verify reimbursement policy alignment",
        "Prepare submission packet"
    ]
    return StepOutcome(success=True, output={"summary": summary, "plan": plan})


def run_reimbursement_flow(task: Task, payload: dict[str, Any], db) -> Task:
    steps = [
        WorkflowStep(name="eligibility_check", action=_eligibility_step, max_retries=1),
        WorkflowStep(name="plan", action=_plan_step, max_retries=0)
    ]
    engine = WorkflowEngine(steps)
    context = WorkflowContext(task=task, payload=payload, db=db)
    return engine.run(context)
