from django.db import models


class Detection(models.Model):
    # Reference value corresponding at the moment in which the system started the process
    record_name = models.CharField(max_length=300)
    # Date in which this record in particular was created
    time_stamp = models.DateTimeField(null=True, blank=True)
    # Original file name
    file_name = models.CharField(max_length=300, null=True, blank=True)
    # File system location of the license plate prediction
    pred_loc = models.CharField(max_length=2000, null=True, blank=True)
    # File system location of the license plate prediction crop
    crop_loc = models.CharField(max_length=2000, null=True, blank=True)
    # Time elapsed in the license plate prediction
    processing_time_pred = models.DecimalField(decimal_places=20, max_digits=30, null=True, blank=True)
    # Time elapsed in the license plate ocr process
    processing_time_ocr = models.DecimalField(decimal_places=20, max_digits=30,null=True, blank=True)
    # ocr result
    ocr_text_result = models.CharField(max_length=500, null=True, blank=True)
    # binary encode64 of the license plate prediction
    #pred_json_base64 = models.CharField(max_length=10000, null=True, blank=True)
    # binary encode64 of the license plate prediction crop
    #crop_json_base64 = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self) -> str:
        return (
            f"record: {self.record_name} || time_stamp:{self.time_stamp} || filename: {self.file_name} || ocr:{self.ocr_text_result}"
        )
