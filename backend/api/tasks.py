from datetime import datetime
from time import sleep

from celery import shared_task


@shared_task
def mytask():
    sleep(5)
    print(f"{datetime.now()}")
    print("----------")
