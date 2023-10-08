from celery import Celery
from celery.utils.log import get_task_logger

# Create a Celery instance
celery = Celery(
    'celery_worker',
    broker='redis://localhost:6380/0',
    backend='redis://localhost:6380/1'
)

# Define a task logger
logger = get_task_logger(__name__)
