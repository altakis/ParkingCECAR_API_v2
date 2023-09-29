import uuid
from typing import Optional, Union

from api.models import Detection
from api.serializers import DetectionSerializer
from django.http import Http404, HttpRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import utils


class DetectionDetailIdRef(APIView):
    """
    Retrieve a detection instance given an specific id_ref.
    """

    def get_objects(self, id_ref: Union[str, uuid.UUID]):
        try:
            return Detection.objects.get(id_ref=id_ref)
        except Detection.DoesNotExist:
            raise Http404
    
    def get(
        self,
        request: Optional[HttpRequest],
        id_ref: Union[str, uuid.UUID],
        format=None,
    ):
        detection = self.get_objects(id_ref)
        serializer = DetectionSerializer(detection)

        return Response(serializer.data)

    def post(
        self,
        request: Optional[HttpRequest],
        id_ref: Union[str, uuid.UUID],
        format=None,
    ):
        detection = self.get_objects(id_ref)
        serializer = DetectionSerializer(detection)

        options = utils.get_base64_query_params(request.data.get("options"))
        if len(options) > 0:
            payload = utils.add_base64_objets_to_response(
                serializer.data, options
            )
        else:
            payload = serializer.data

        return Response(payload)

    def put(
        self, request: HttpRequest, id_ref: Union[str, uuid.UUID], format=None
    ):
        detection = self.get_object(id_ref)
        serializer = DetectionSerializer(detection, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self,
        request: Optional[HttpRequest],
        id_ref: Union[str, uuid.UUID],
        format=None,
    ):
        detection = self.get_object(id_ref)
        detection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
