from django.contrib.auth.models import User
from api.models import Detection
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from dummy_data.detections_dummy_data import all_detections_dummy_data

DETECTIONS_ALL_CREATE_ENDPOINT = "/api/v1/detections/"
DETECTION_DETAIL_ID = "/api/v1/detections/id"
DETECTION_DETAIL_FILENAME = "/api/v1/detections/filename"
DETECTION_DETAIL_IDREF = "/api/v1/detections/ref"


class APIDetectionTestCase(APITestCase):
    """
    Test suite for Detections
    """

    def setUp(self):
        for element in all_detections_dummy_data:
            Detection.objects.create(
                id=element.get("id"),
                id_ref=element.get("id_ref"),
                record_name=element.get("record_name"),
                time_stamp=element.get("time_stamp"),
                file_name=element.get("file_name"),
                pred_loc=element.get("pred_loc"),
                crop_loc=element.get("crop_loc"),
                processing_time_pred=element.get("processing_time_pred"),
                processing_time_ocr=element.get("processing_time_ocr"),
                ocr_text_result=element.get("ocr_text_result"),
            )

        self.detections = Detection.objects.all()

        # The app uses token authentication
        # self.token = Token.objects.get(user=self.user)
        self.client = APIClient()

        # We pass the token in all calls to the API
        # self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_all_items(self):
        """
        test Detection list method
        """
        self.assertEqual(self.detections.count(), 8)
        response = self.client.get(DETECTIONS_ALL_CREATE_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_detection_by_id(self):
        """
        test DetectionDetailId retrieve method
        """
        for detection in self.detections:
            response = self.client.get(f"{DETECTION_DETAIL_ID}/{detection.id}/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_detection_by_filename(self):
        """
        test DetectionDetailFileName retrieve method
        """
        for detection in self.detections:
            response = self.client.get(
                f"{DETECTION_DETAIL_FILENAME}/{detection.file_name}/"
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_detection_by_idref(self):
        """
        test DetectionDetailIdRef retrieve method
        """
        for detection in self.detections:
            response = self.client.get(
                f"{DETECTION_DETAIL_IDREF}/{detection.id_ref}/"
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_all_detections_by_id(self):
        """
        test DetectionDetailId delete method
        """
        for detection in self.detections:
            response = self.client.delete(
                f"{DETECTION_DETAIL_ID}/{detection.id}/"
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(response.data, None)

    def test_get_all_items_after_delete_all_operation(self):
        expected_count = 8
        response = self.client.get(DETECTIONS_ALL_CREATE_ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.detections.count(), expected_count)

        for detection in self.detections:
            expected_count = expected_count - 1

            response = self.client.delete(
                f"{DETECTION_DETAIL_ID}/{detection.id}/"
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(response.data, None)

            response = self.client.get(DETECTIONS_ALL_CREATE_ENDPOINT)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), expected_count)
