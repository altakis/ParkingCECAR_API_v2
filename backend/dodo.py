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

def task_rundevpub():
    return {
        "actions": [CmdAction(f"{POETRY_ENV_RUN} {PYTHON_SCRIPT_CMD} manage runserver 0.0.0.0:8000")],
        'verbosity': 2,
    }
