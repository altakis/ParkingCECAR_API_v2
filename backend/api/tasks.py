import logging
from uuid import UUID

from celery import shared_task
from detector_utils import detector_interface

from .serializers import DetectionSerializer


@shared_task
def background_detection(id_ref: UUID, data: dict):
    """
    Detects license plates in images and saves the results to the database.

    The id_ref and data dict are passed to the shared task background_detection.
    The image is extracted from the data dict and passed to detect_license which handles
    the actual license plate detection using the Detector class. The results are returned and
    the id_ref is added. Finally, save_detection serializes the data and saves it to the database.

    Args:
        id_ref (UUID): The unique id for this detection.
        data (dict): The data dict containing the source image file path.
    """
    # Detect license plate
    detection = detect_license(data["src_file"])

    # Add custom generated reference id to payload
    detection["detection"]["id_ref"] = id_ref

    logging.info(detection)

    # Save detection result
    save_detection(detection.get("detection"))


def detect_license(src_file):
    detector = detector_interface.DetectorInterface()
    return detector.detect_license_from_fs_location(src_file)


def save_detection(detection):
    serializer = DetectionSerializer(data=detection)
    if serializer.is_valid(raise_exception=True):
        logging.info(serializer.validated_data)
        serializer.save()
