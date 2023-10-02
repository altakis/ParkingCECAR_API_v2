import uuid
from typing import Optional, Union

from api.models import Detection
from api.serializers import DetectionSerializer
from django.http import Http404, HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response


class DetectionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a detection instance.
    """

    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    @extend_schema(responses=DetectionSerializer)
    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    @extend_schema(responses=DetectionSerializer)
    def put(self, request, *args, **kwargs):
        return self.update(self, request, *args, **kwargs)

    @extend_schema(responses=DetectionSerializer)
    def delete(self, request, *args, **kwargs):
        return self.destroy(self, request, *args, **kwargs)
