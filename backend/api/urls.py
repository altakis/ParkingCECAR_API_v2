from django.urls import path

from . import views as api_views


urlpatterns = [
    path("detections/", api_views.detection_endpoints, name="detections_list"),
    path("detections/id/<str:id>", api_views.detection_detail, name="detection_detal_by_id"),
    path("detections/filename/<str:file_name>", api_views.detection_detail_name, name="detection_detal_by_file_name"),
    path("detections/ref/<str:id_ref>", api_views.detection_detail_id_ref),
]
