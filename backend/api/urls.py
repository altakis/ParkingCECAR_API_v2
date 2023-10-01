from django.urls import path

from . import views as api_views


urlpatterns = [
    path(
        "detections/",
        api_views.DetectionList.as_view(),
        name="detections_list",
    ),
    path(
        "detections/id/<str:id>/",
        api_views.DetectionDetail.as_view(),
        name="detection_detal_by_id",
    ),
    path(
        "detections/filename/<str:file_name>/",
        api_views.DetectionDetailFileName.as_view(),
        name="detection_detal_by_file_name",
    ),
    path(
        "detections/ref/<str:id_ref>/",
        api_views.DetectionDetailIdRef.as_view(),
    ),
]
