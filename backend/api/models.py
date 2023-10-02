import uuid

from django.db import models


class Detection(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    # Reference value corresponding at the moment in which
    # the system started the process
    id_ref = models.UUIDField(default=uuid.uuid4)
    record_name = models.CharField(max_length=300, null=True, blank=True)
    # Date in which this record in particular was created
    time_stamp = models.DateTimeField(null=True, blank=True)
    # Original file name
    file_name = models.CharField(max_length=300, null=True, blank=True)
    # File system location of the license plate prediction
    pred_loc = models.CharField(max_length=2000, null=True, blank=True)
    # File system location of the license plate prediction crop
    crop_loc = models.CharField(max_length=2000, null=True, blank=True)
    # Time elapsed in the license plate prediction
    processing_time_pred = models.DecimalField(
        decimal_places=20, max_digits=30, null=True, blank=True
    )
    # Time elapsed in the license plate ocr process
    processing_time_ocr = models.DecimalField(
        decimal_places=20, max_digits=30, null=True, blank=True
    )
    ocr_text_result = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        attributes_list_formatted = f"record: {self.record_name} || "
        attributes_list_formatted += f"time_stamp:{self.time_stamp} || "
        attributes_list_formatted += f"filename: {self.file_name} || "
        attributes_list_formatted += f"ocr:{self.ocr_text_result}"
        return attributes_list_formatted
