import uuid
from typing import Optional, Union

from api.models import Detection
from api.serializers import DetectionSerializer
from django.http import Http404, HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import mixins


class DetectionDetail(generics.GenericAPIView):
    """
    Retrieve, update or delete a detection instance.
    """

    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    @extend_schema(exclude=True)
    def get_object(self, id: Union[str, uuid.UUID]):
        try:
            return Detection.objects.get(id=id)
        except Detection.DoesNotExist:
            raise Http404

    @extend_schema(responses=DetectionSerializer)
    def get(
        self,
        request: Optional[HttpRequest],
        id: Union[str, uuid.UUID],
        format=None,
    ):
        detection = self.get_object(id)
        serializer = DetectionSerializer(detection)
        return Response(serializer.data)

    @extend_schema(responses=DetectionSerializer)
    def put(self, request: HttpRequest, id: Union[str, uuid.UUID], format=None):
        detection = self.get_object(id)
        serializer = DetectionSerializer(detection, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=DetectionSerializer)
    def delete(
        self,
        request: Optional[HttpRequest],
        id: Union[str, uuid.UUID],
        format=None,
    ):
        detection = self.get_object(id)
        detection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
