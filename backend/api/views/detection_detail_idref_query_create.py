import uuid
from typing import Optional, Union

from api.models import Detection
from api.serializers import DetectionSerializer, IdRefOptionsSerializer
from detector_utils.inference_interface import DetectorInterface
from django.http import HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins
from rest_framework.response import Response


class DetectionDetailIdRef(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Retrieve a detection instance given an specific id_ref.
    """

    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer
    lookup_field = "id_ref"

    @extend_schema(responses=DetectionSerializer)
    def get(self, request, *args, **kwargs):
        """Retrieves a single detection record that matches the id_ref given

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.retrieve(self, request, *args, **kwargs)

    @extend_schema(
        responses=DetectionSerializer,
        request=IdRefOptionsSerializer,
    )
    def post(
        self,
        request: Optional[HttpRequest],
        id_ref: Union[str, uuid.UUID],
        format=None,
    ):
        """Retrieves an specific detection record given an id_ref.
        Aditionally, this method also packages and sends a base64 string
        containing a image object across a REST response.

        Args:
            request (Optional[HttpRequest]): _description_
            id_ref (Union[str, uuid.UUID]): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        detection = self.get_object()
        serializer = DetectionSerializer(detection)

        payload = DetectorInterface.check_for_base64_request_options(
            serializer.data, request.data
        )

        return Response(payload)
