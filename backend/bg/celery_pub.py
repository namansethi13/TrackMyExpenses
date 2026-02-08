from bg.base import TaskPublisherBase
from cel.app import celery_app

class CeleryTaskPublisher(TaskPublisherBase):

    def publish(self, task_name, args=None, kwargs=None, countdown=None):
        celery_app.send_task(
            task_name,
            args=args or [],
            kwargs=kwargs or {},
            countdown=countdown,
        )
