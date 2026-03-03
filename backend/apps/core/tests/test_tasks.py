from apps.core.tasks import health_check_task


def test_health_check_task_returns_structured_result():
    result = health_check_task.apply().get()

    assert result == {
        "status": "ok",
        "message": "Celery worker executed successfully",
    }
