#!/usr/bin/env python3
# coding: utf-8
# pylint:disable=unused-wildcard-import
from doit.action import CmdAction

POETRY_ENV_RUN = "poetry run"
PYTHON_SCRIPT_CMD = "python -m"

def task_rundev():
    return {
        "actions": [CmdAction(f"{POETRY_ENV_RUN} {PYTHON_SCRIPT_CMD} manage runserver")],
        'verbosity': 2,
    }

def task_celery_run():
    return {
        "actions": [CmdAction(f"{POETRY_ENV_RUN} {PYTHON_SCRIPT_CMD} celery -A core worker -P gevent")],
        'verbosity': 2,
    }

def task_celery_info():
    return {
        "actions": [CmdAction(f"{POETRY_ENV_RUN} {PYTHON_SCRIPT_CMD} celery -A core worker -l INFO -P gevent")],
        'verbosity': 2,
    }