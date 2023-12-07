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


class DetectionPOSTOptionsSerializer(serializers.Serializer):
    src_file = serializers.CharField(
        required=False,
        max_length=None,
        min_length=None,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
    )
    src_base64 = serializers.CharField(
        required=False,
        max_length=None,
        min_length=None,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
    )
    src_base64_file_name = serializers.CharField(
        required=False,
        max_length=None,
        min_length=None,
        allow_blank=True,
        allow_null=True,
        trim_whitespace=True,
    )
    # Return base64 strings of results
    pred = serializers.BooleanField(required=False, allow_null=True)
    crop = serializers.BooleanField(required=False, allow_null=True)
