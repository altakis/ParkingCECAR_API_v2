import logging
import uuid

from api.models import Detection
from api.serializers import DetectionPOSToptionsSerializer, DetectionSerializer
from api.tasks import background_detection
from core import celery_utils
from detector_utils import FileManagerUtil, detector_interface
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

    @extend_schema(
        responses=DetectionSerializer,
        request=DetectionPOSToptionsSerializer,
    )
    def post(self, request, format=None):
        """Toma el origen en el sistema de archivos de una imagen y detecta
        la presencia de placas de licencia vehicular.
        """
        logging.debug(request)
        data = request.data
        src_file_exist = "src_file" in data
        src_base64_exist = "src_base64" in data
        if src_file_exist or src_base64_exist:
            # operation code: int default=2
            # 0: use src_file
            # 1: use base64_src
            # 2: Both src parameter are malformed
            operation_code = 2
            if src_file_exist:
                src_file = data["src_file"]
                check_path_validity = FileManagerUtil.FileManagerUtil.is_valid_file_path(
                    src_file
                )
                if check_path_validity:
                    operation_code = 0
            elif src_base64_exist and (not len(data["src_base64"]) == 0):
                src_file = data["src_base64"]
                operation_code = 1

            # Shortcircuit operation if operation_code is equal to 2.
            if operation_code == 2:
                return Response(
                    {"error": "Malformed request", "data": data},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Otherwise if operation_code is 1 then transform base64_string
            # to an image and save it to the tmp_folder
            if operation_code == 1:
                if "src_base64_file_name" in data:
                    base64_filename = data["src_base64_file_name"]
                else:
                    base64_filename = None
                data[
                    "src_file"
                ] = FileManagerUtil.FileManagerUtil().save_base64_string_to_image_file_to_tmp_folder(
                    base64_str=src_file, base64_file_name=base64_filename
                )
            # if operation_code is 0 then do nothing.
            # if operation_code == 0: pass

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

            payload = {}
            payload["id_ref"] = id_field
            payload[
                "msg"
            ] = "Check back with that uuid in 30 secs at the endpoint /detections/ref/<uuid:id_ref>"

            return Response(payload, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "Missing any src file parameters.", "data": data},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(exclude=True)
    def detector_funtion(self, id_field, data):
        detector_ins = detector_interface.Detector()
        logging.debug(data)
        payload = detector_ins.detect_license_from_fs_location(
            fs_location=data["src_file"]
        )
        logging.debug(payload)
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
