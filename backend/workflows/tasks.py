import uuid

from workflows.celery_app import celery_app


@celery_app.task(name="workflows.tasks.process_intake")
def process_intake(summary: str, ai_brief: str) -> str:
    workflow_id = str(uuid.uuid4())
    # TODO: persist workflow state + notify agents
    return workflow_id


def enqueue_intake(summary: str, ai_brief: str) -> str:
    async_result = process_intake.delay(summary, ai_brief)
    return async_result.id
