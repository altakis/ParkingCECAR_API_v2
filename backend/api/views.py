import uuid

from detector_utils import detector_interface
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Detection
from .serializers import DetectionSerializer


@api_view(http_method_names=["GET", "POST"])
def detection_endpoints(request, format=None):
    if request.method == "GET":
        return detection_list(request, format)

    if request.method == "POST":
        return detection_detect(request, format)


def detection_list(request, format=None):
    detections = Detection.objects.all()
    serializer = DetectionSerializer(detections, many=True)
    return Response({"detections": serializer.data})


def detection_detect(request, format=None):
    data = request.data

    detector_ins = detector_interface.Detector()
    payload = detector_ins.detect_license_from_fs_location(
        fs_location=data["data"]["src_file"]
    )
    id_field = uuid.uuid4()
    payload["id"] = id_field
    # print(f'payload: {payload}')
    serializer = DetectionSerializer(data=payload.get("detection"))
    """ print(f'serializer: valid? {serializer.is_valid()}')
    print(serializer.errors)
    print(serializer.validated_data) """
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response({"message": "error"}, status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=["GET", "PUT", "DELETE"])
def detection_detail(request, id, format=None):
    try:
        detection = Detection.objects.get(pk=id)
    except Detection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DetectionSerializer(detection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = DetectionSerializer(detection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        print(detection.delete())
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=["GET", "PUT", "DELETE"])
def detection_detail_name(request, file_name, format=None):
    try:
        detection = Detection.objects.filter(file_name_containts=file_name)
    except Detection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DetectionSerializer(detection)
        return Response(serializer.data)
    ###
    # TODO: check if needed or simply let this be a query method and let the other operations be performed by the id endpoint
    pending = """ elif request.method == "PUT":
        serializer = DetectionSerializer(detection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        print(detection.delete())
        return Response(status=status.HTTP_204_NO_CONTENT) """
