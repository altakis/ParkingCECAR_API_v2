from celery import shared_task
from detector_utils import detector_interface

from .serializers import DetectionSerializer


@shared_task
def background_detection(id_field, data):
    detector_ins = detector_interface.Detector()
    payload = detector_ins.detect_license_from_fs_location(
        fs_location=data["data"]["src_file"]
    )
    payload["detection"]["id_ref"] = id_field

    # print(f"payload: {payload}")
    serializer = DetectionSerializer(data=payload.get("detection"))
    """ print("1. validity--------------------------------")
    print(f"serializer: valid? {serializer.is_valid()}")
    print("2. errors  --------------------------------")
    print(serializer.errors)
    print("3. data    --------------------------------")
    print(serializer.validated_data)
    print("-------------------------------------------") """
    if serializer.is_valid():
        serializer.save()
