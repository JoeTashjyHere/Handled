from typing import Callable

from models.task import Task, TaskType
from workflows.government_form_flow import run_government_form_flow
from workflows.reimbursement_flow import run_reimbursement_flow
from workflows.scheduling_flow import run_scheduling_flow
from workflows.tax_filing_flow import run_tax_filing_flow

WorkflowRunner = Callable[[Task, dict, object], Task]


def get_workflow_runner(task_type: str) -> WorkflowRunner:
    mapping: dict[str, WorkflowRunner] = {
        TaskType.reimbursement.value: run_reimbursement_flow,
        TaskType.scheduling.value: run_scheduling_flow,
        TaskType.government_form.value: run_government_form_flow,
        TaskType.tax_filing.value: run_tax_filing_flow
    }
    if task_type not in mapping:
        raise ValueError(f"No workflow registered for task type '{task_type}'.")
    return mapping[task_type]
