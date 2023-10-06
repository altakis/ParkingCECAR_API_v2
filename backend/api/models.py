from uuid import uuid4

from django.db import models


class Detection(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True
    )
    # Reference value corresponding at the moment in which
    # the system started the process
    id_ref = models.UUIDField(default=uuid4)
    record_name = models.TextField(null=True, blank=True)
    # Date in which this record in particular was created
    time_stamp = models.DateTimeField(null=True, blank=True)
    # Original file name
    file_name = models.TextField(null=True, blank=True)
    # File system location of the license plate prediction
    pred_loc = models.TextField(null=True, blank=True)
    # File system location of the license plate prediction crop
    crop_loc = models.TextField(null=True, blank=True)
    # Time elapsed in the license plate prediction
    processing_time_pred = models.DecimalField(
        decimal_places=20, max_digits=30, null=True, blank=True
    )
    # Time elapsed in the license plate ocr process
    processing_time_ocr = models.DecimalField(
        decimal_places=20, max_digits=30, null=True, blank=True
    )
    ocr_text_result = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"record: {self.record_name} time: {self.time_stamp} file: {self.file_name} ocr: {self.ocr_text_result}"
