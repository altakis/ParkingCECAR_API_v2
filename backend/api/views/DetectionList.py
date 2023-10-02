import logging
import uuid

from api.models import Detection
from api.serializers import DetectionSerializer
from api.tasks import background_detection
from core import celery_utils
from detector_utils import detector_interface
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, status
from rest_framework.response import Response


class DetectionList(mixins.ListModelMixin, generics.GenericAPIView):
    """
    List all detections, or create a new detection.
    """

    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    @extend_schema(responses=DetectionSerializer)
    def get(self, request, *args, **kwargs):
        """Retrieves a list of all the available detections.

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.list(self, request, *args, **kwargs)

    @extend_schema(responses=DetectionSerializer)
    def post(self, request, format=None):
        """Creates a detection record

        Args:
            request (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        data = request.data

        id_field = uuid.uuid4()

        worker_status = celery_utils.get_worker_status()
        # print(f"Testing worker status: {worker_status}")
        worker_availability = worker_status.get("availability")
        # print(f"Testing worker availability: {worker_availability}")
        worker_up_flag = False
        if worker_availability is not None:
            if len(worker_availability) > 0:
                background_detection.delay(id_field, data)
                worker_up_flag = True
        else:
            logging.warning("Celery-redis worker down")

        if not worker_up_flag:
            self.detector_funtion(id_field, data)

        payload = {}
        payload["id_ref"] = id_field
        payload[
            "msg"
        ] = "Check back with that uuid in 30 secs at the endpoint /detections/ref/<uuid:id_ref>"

        return Response(payload, status=status.HTTP_201_CREATED)

    @extend_schema(exclude=True)
    def detector_funtion(self, id_field, data):
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
        if serializer.is_valid(raise_exception=True):
            serializer.save()
