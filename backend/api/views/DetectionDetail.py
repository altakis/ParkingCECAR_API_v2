import uuid
from typing import Optional, Union

from api.models import Detection
from api.serializers import DetectionSerializer
from django.http import Http404, HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class DetectionDetail(APIView):
    """
    Retrieve, update or delete a detection instance.
    """

    @extend_schema(exclude=True)
    def get_object(self, pk: Union[str, uuid.UUID]):
        try:
            return Detection.objects.get(id=pk)
        except Detection.DoesNotExist:
            raise Http404

    @extend_schema(responses=DetectionSerializer)
    def get(
        self,
        request: Optional[HttpRequest],
        pk: Union[str, uuid.UUID],
        format=None,
    ):
        detection = self.get_object(pk)
        serializer = DetectionSerializer(detection)
        return Response(serializer.data)

    @extend_schema(responses=DetectionSerializer)
    def put(self, request: HttpRequest, pk: Union[str, uuid.UUID], format=None):
        detection = self.get_object(pk)
        serializer = DetectionSerializer(detection, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=DetectionSerializer)
    def delete(
        self,
        request: Optional[HttpRequest],
        pk: Union[str, uuid.UUID],
        format=None,
    ):
        detection = self.get_object(pk)
        detection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
