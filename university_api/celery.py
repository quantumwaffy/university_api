import os

from celery import Celery
from celery.schedules import crontab

from university_api import celeryconfig, settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "university_api.settings")

app = Celery("university_api")

app.config_from_object(celeryconfig)

app.conf.task_routes = {
    "api.tasks.*": {"queue": "university_api", "routing_key": "university_api"},
}

app.conf.enable_utc = False

app.conf.beat_schedule = {
    "send_tomorrow_schedule": {
        "task": "university_api.tasks.send_lecture_schedule_to_email",
        "schedule": crontab(hour=20, minute=30, day_of_week=[0, 1, 2, 3, 4]),
    },
}
app.autodiscover_tasks(settings.INSTALLED_APPS)

if __name__ == "__main__":
    app.start()
