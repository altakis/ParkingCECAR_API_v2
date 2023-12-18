import datetime
import logging
import time

import cv2
import easyocr
from PIL import Image
from ultralytics import YOLO

from .image_utils import PIL2CV2, adjust_dimensions
from .ocr_utils import get_ocr_output


class LicenseDetector:
    def __init__(self, gpu_available=False, ocr_verbose=False) -> None:
        self._model = YOLO(
            model="detector_utils/ml_models/yolov8n_license_detector_20e.onnx",
            task="detect",
        )
        self._reader = easyocr.Reader(
            ["en"], gpu=gpu_available, verbose=ocr_verbose
        )

    @property
    def model(self) -> YOLO:
        return self._model

    @model.setter
    def model(self, model_name) -> None:
        return self.model

    @property
    def reader(self) -> easyocr.Reader:
        return self._reader

    def make_prediction(self, img):
        img = adjust_dimensions(img)

        return self.model.predict(source=img, imgsz=416, save=True)

    def visualize_prediction(
        self, img: Image.Image, output_list, threshold=0.7
    ):
        # convert PIL.Image to OpenCV format
        img_cv = PIL2CV2(img)
        # crop_error values:
        # 0 = No error,
        # 1 = cropping error,
        # 2 = no license found in img
        crop_error = 0.0
        crop_img_list = []
        for object_data in output_list[0].boxes.data:
            x1, y1, x2, y2, score, class_id = object_data

            if class_id == 0 and score > threshold:
                try:
                    crop_img_list.append(
                        [
                            img_cv[int(y1) : int(y2), int(x1) : int(x2), :],
                            {
                                x1: x1,
                                y1: y1,
                                x2: x2,
                                y2: y2,
                                score: score,
                                class_id: class_id,
                            },
                        ]
                    )
                except Exception as e:
                    logging.error(e, exc_info=True)
                    try:
                        crop_img_list.append(img)
                        crop_error += 0.1
                    except Exception as e:
                        logging.error(e, exc_info=True)
                        continue

        if len(crop_img_list) == 0:
            crop_error = 2
            crop_img_list = [img]
        else:
            # class labels extracted from model configuration
            id2label_dict = {0: "license-plate", 1: "vehicle"}
            for crop_data in crop_img_list:
                img_array = crop_data[0]
                x1, y1, x2, y2, score, class_id = crop_data[1].values()
                height, width, _ = img_array.shape
                # linewidth and thickness
                lw = max(
                    round(sum((height, width)) / 2 * 0.003), 2
                )  # Line width.
                tf = max(lw - 1, 1)  # Font thickness.
                cv2.rectangle(
                    img_array,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    thickness=tf,
                )
                FONT_SCALE = 2e-3
                cv2.putText(
                    img=img_array,
                    text=f"{id2label_dict[class_id]}: {score:0.2f}",
                    org=(int(x1), int(y1)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=min(width, height) * FONT_SCALE,
                    color=(0, 255, 255),
                    thickness=tf,
                )

        license_located_img = img_cv[int(y1) : int(y2), int(x1) : int(x2), :]
        if crop_error == 2:
            return license_located_img, license_located_img, crop_error
        return license_located_img, crop_img_list, crop_error

    def detect_objects(self, image_input, threshold):
        # Time process
        start_time_detection = time.perf_counter()

        # Make prediction
        processed_outputs = self.make_prediction(image_input)[0]

        # Visualize prediction
        viz_img, crop_img, crop_error = self.visualize_prediction(
            image_input, processed_outputs, threshold
        )
        detection_process_time = time.perf_counter() - start_time_detection

        # OCR license
        (
            license_text_ocr_result,
            ocr_process_time,
        ) = get_ocr_output(self.reader, crop_img, crop_error)

        # package data and return
        time_stamp = datetime.datetime.now()

        return {
            "record_name": f"{time_stamp}_",
            "time_stamp": time_stamp,
            "viz_img": viz_img,
            "crop_img": crop_img,
            "ocr_text_result": str(license_text_ocr_result),
            "processing_time_pred": round(detection_process_time, 20),
            "processing_time_ocr": round(ocr_process_time, 20),
        }
