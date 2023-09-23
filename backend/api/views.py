import uuid

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Detection
from .serializers import DetectionSerializer
from .tasks import background_detection


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

    id_field = uuid.uuid4()
    #print(id_field)
    background_detection.delay(id_field, data)
    payload = {}
    payload["id_ref"] = id_field
    payload["msg"] = "Check back with that uuid in 30 secs at the endpoint /detections/ref/<uuid:id_ref>"

    return Response(payload, status=status.HTTP_201_CREATED)


@api_view(http_method_names=["GET", "PUT", "DELETE"])
def detection_detail(request, id, format=None):
    try:
        detection = Detection.objects.get(id=id)
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
        detection = Detection.objects.filter(file_name__contains=file_name)
    except Detection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DetectionSerializer(detection)
        return Response(serializer.data)
    ###
    # TODO: check if needed or simply let this be a query method and let the other operations be performed by the id endpoint
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
def detection_detail_id_ref(request, id_ref, format=None):
    try:
        detection = Detection.objects.get(id_ref=id_ref)
    except Detection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = DetectionSerializer(detection)
        return Response(serializer.data)
    ###
    # TODO: check if needed or simply let this be a query method and let the other operations be performed by the id endpoint
    elif request.method == "PUT":
        serializer = DetectionSerializer(detection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        print(detection.delete())
        return Response(status=status.HTTP_204_NO_CONTENT)