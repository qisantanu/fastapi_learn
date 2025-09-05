from celery import Celery
import logging

app = Celery('worker', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'periodic-task': {
        'task': 'celery_app.periodic_log_task',
        'schedule': 15.0,  # every 15 seconds
    },
}

@app.task
def periodic_log_task():
    logging.info("Periodic task executed - Hello from Celery worker!")
    return "Task completed"
