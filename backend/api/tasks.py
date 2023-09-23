from datetime import datetime
from time import sleep

from celery import shared_task
from detector_utils import detector_interface

from .serializers import DetectionSerializer

@shared_task
def background_detection(detector_function, id_field, data):
    detector_function(id_field, data)

def get_worker_status():
    from core.celery_app import app
    worker_status = app.control.inspect().ping()

    is_worker_running = bool(worker_status)
    
    return is_worker_running