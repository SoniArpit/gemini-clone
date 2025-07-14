from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.gemini_tasks"
    ]
)
celery_app.conf.update(task_routes={
    "app.tasks.gemini_tasks.*": {"queue": "gemini"},
})