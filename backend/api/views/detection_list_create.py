import logging
import uuid

from api.models import Detection
from api.serializers import DetectionPOSTOptionsSerializer, DetectionSerializer
from detector_utils import file_system_utils, inference_interface
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
        request=DetectionPOSTOptionsSerializer,
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
                check_path_validity = (
                    file_system_utils.FileSystemInterface.is_valid_file_path(
                        src_file
                    )
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
                ] = file_system_utils.FileSystemInterface().save_base64_string_to_image_file_to_tmp_folder(
                    base64_str=src_file, base64_file_name=base64_filename
                )
            # if operation_code is 0 then do nothing.
            # if operation_code == 0: pass

            id_field = uuid.uuid4()

            payload_data = self.detector_funtion(id_field, data)

            payload = {}
            payload["id_ref"] = id_field
            payload["data"] = payload_data

            return Response(payload, status=status.HTTP_201_CREATED)
        return Response(
            {"error": "Missing any src file parameters.", "data": data},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(exclude=True)
    def detector_funtion(self, id_field, data):
        detector_ins = inference_interface.DetectorInterface()
        logging.debug(data)
        payload = detector_ins.detect_license_from_fs_location(
            fs_location=data["src_file"]
        )

        payload["detection"]["id_ref"] = id_field
        logging.debug(payload)
        payload_data = payload.get("detection")

        serializer = DetectionSerializer(data=payload_data)
        if serializer.is_valid(raise_exception=True):
            logging.info(serializer.validated_data)
            serializer.save()
            return payload_data

        return None 
