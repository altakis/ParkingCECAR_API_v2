from rest_framework import serializers

from .models import Detection


class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = [
            "id",
            "id_ref",
            "record_name",
            "time_stamp",
            "file_name",
            "pred_loc",
            "crop_loc",
            "processing_time_pred",
            "processing_time_ocr",
            "ocr_text_result",
        ]

class DetectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = [
            "id",
            "id_ref",
            "record_name",
            "time_stamp",
            "file_name",
            "pred_loc",
            "crop_loc",
            "processing_time_pred",
            "processing_time_ocr",
            "ocr_text_result",
        ]

class IdRefOptionsSerializer(serializers.Serializer):
    pred = serializers.BooleanField()
    crop = serializers.BooleanField()