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
        """Toma el origen en el sistema de archivos de una imagen y detecta
        la presencia de placas de licencia vehicular.
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
            operation_code = self.detector_funtion(id_field, data)
        if operation_code == 0:
            return Response(
                {"error": "Malformed request", "data": request.data},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = {}
        payload["id_ref"] = id_field
        payload[
            "msg"
        ] = "Check back with that uuid in 30 secs at the endpoint /detections/ref/<uuid:id_ref>"

        return Response(payload, status=status.HTTP_201_CREATED)

    @extend_schema(exclude=True)
    def detector_funtion(self, id_field, data):
        detector_ins = detector_interface.Detector()
        logging.info(data)
        payload = detector_ins.detect_license_from_fs_location(
            fs_location=data["src_file"]
        )
        logging.info(payload)
        if len(payload) == 0:
            return 0

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
        return 1
