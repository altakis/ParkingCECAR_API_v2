import logging
import traceback

from celery import current_app


def get_worker_status():
    i = current_app.control.inspect()
    result = {
        "availability": None,
    }
    try:
        availability = i.ping()
        stats = i.stats()
        registered_tasks = i.registered()
        active_tasks = i.active()
        scheduled_tasks = i.scheduled()
        result = {
            "availability": availability,
            "stats": stats,
            "registered_tasks": registered_tasks,
            "active_tasks": active_tasks,
            "scheduled_tasks": scheduled_tasks,
        }
    except Exception as e:
        logging.error(traceback.format_exc())

    return result
