import logging
import os

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger

from .TaskFormatter import TaskFormatter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")

logger = logging.getLogger(__name__)


@after_setup_logger.connect
def setup_loggers(*args, **kwargs):
    logger = logging.getLogger()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # StreamHandler
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # FileHandler
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent
    LOGGING_DIR = os.path.join(BASE_DIR, "logs")
    LOG_FILE = os.path.join(LOGGING_DIR, "celery_logs.log")
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


@after_setup_task_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    for handler in logger.handlers:
        handler.setFormatter(
            TaskFormatter(
                "%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)


app.autodiscover_tasks()
