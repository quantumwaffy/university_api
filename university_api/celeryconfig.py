from kombu import Exchange, Queue

from . import settings

broker_url = settings.CELERY_BROKER

task_default_queue = "university_api"

task_queues = (Queue("university_api", Exchange("university_api"), routing_key="university_api"),)

imports = "api.tasks"

try:
    from .local_settings_celery import *  # noqa
except ImportError:
    pass
