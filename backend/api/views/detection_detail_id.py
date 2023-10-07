from api.models import Detection
from api.serializers import DetectionSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.response import Response


class DetectionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a detection instance.
    """

    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer
    lookup_field = "id"

    @extend_schema(responses=DetectionSerializer)
    def get(self, request, *args, **kwargs):
        """Retrieve a detection instance given a specific id"""
        return self.retrieve(self, request, *args, **kwargs)

    @extend_schema(responses=DetectionSerializer)
    def put(self, request, *args, **kwargs):
        """Update a detection instance given a specific id"""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses=DetectionSerializer)
    def delete(self, request, *args, **kwargs):
        """Delete a detection instance given a specific id."""
        return self.destroy(self, request, *args, **kwargs)
