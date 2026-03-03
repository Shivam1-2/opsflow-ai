import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="apps.core.tasks.health_check_task")
def health_check_task() -> dict[str, str]:
    logger.info("Executing Celery health_check_task")
    return {
        "status": "ok",
        "message": "Celery worker executed successfully",
    }
