from django.core.management.base import BaseCommand

from apps.core.tasks import health_check_task


class Command(BaseCommand):
    help = "Enqueue the Celery health_check_task and wait for the worker result."

    def handle(self, *args, **options):
        async_result = health_check_task.delay()
        self.stdout.write(f"Enqueued health_check_task id={async_result.id}")
        result = async_result.get(timeout=15)
        self.stdout.write(self.style.SUCCESS(f"Task result: {result}"))
