import uuid
from typing import Optional, Union

from api.models import Detection
from api.serializers import DetectionSerializer
from django.http import Http404, HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import utils


class DetectionDetailIdRef(APIView):
    """
    Retrieve a detection instance given an specific id_ref.
    """

    def get_object(self, id_ref: Union[str, uuid.UUID]):
        try:
            return Detection.objects.get(id_ref=id_ref)
        except Detection.DoesNotExist:
            raise Http404

    @extend_schema(responses=DetectionSerializer)
    def get(
        self,
        request: Optional[HttpRequest],
        id_ref: Union[str, uuid.UUID],
        format=None,
    ):
        """Retrieves a single detection record that matches the id_ref given

        Args:
            request (Optional[HttpRequest]): Request info object carrying headers and request metadata.
            id_ref (Union[str, uuid.UUID]): UUID asociate identifier for a detection record.
            format (_type_, optional): System required config object that can help in specifying the format version .json|.html of the response. Defaults to None.

        Returns:
            _type_: _description_
        """
        detection = self.get_object(id_ref)
        serializer = DetectionSerializer(detection)

        return Response(serializer.data)

    @extend_schema(responses=DetectionSerializer)
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
        detection = self.get_object(id_ref)
        serializer = DetectionSerializer(detection)

        options = utils.get_base64_query_params(request.data.get("options"))
        if len(options) > 0:
            payload = utils.add_base64_objets_to_response(
                serializer.data, options
            )
        else:
            payload = serializer.data

        return Response(payload)

    @extend_schema(responses=DetectionSerializer)
    def put(
        self, request: HttpRequest, id_ref: Union[str, uuid.UUID], format=None
    ):
        """Updates a specific detection record given an id_ref

        Args:
            request (HttpRequest): _description_
            id_ref (Union[str, uuid.UUID]): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        detection = self.get_object(id_ref)
        serializer = DetectionSerializer(detection, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=DetectionSerializer)
    def delete(
        self,
        request: Optional[HttpRequest],
        id_ref: Union[str, uuid.UUID],
        format=None,
    ):
        """Deletes a specific detection record given an id_ref

        Args:
            request (Optional[HttpRequest]): _description_
            id_ref (Union[str, uuid.UUID]): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        detection = self.get_object(id_ref)
        detection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
