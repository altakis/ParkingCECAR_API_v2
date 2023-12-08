import datetime
import io
import logging
import time
from typing import List

import cv2
import easyocr
import requests
import torch
import validators
from numpy import asarray
from PIL import Image
from .image_utils import fig2img, get_original_image
from .ocr_utils import get_ocr_output
from ultralytics import YOLO


class LicenseDetector:
    def __init__(self, gpu_available=False, ocr_verbose=False) -> None:
        self._model = YOLO("./ml_models/yolov8n_license_detector_20e.onnx")
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
        return self.model(img, stream=True)

    def visualize_prediction(
        self, img, output_dict, threshold=0.5, id2label=None
    ):
        keep = output_dict["scores"] > threshold
        boxes = output_dict["boxes"][keep].tolist()
        scores = output_dict["scores"][keep].tolist()
        labels = output_dict["labels"][keep].tolist()

        # Crops located license img for later ocr processing
        # crop_error values: 0 = None, 1 = cropping error, 2 = not found license
        crop_error = 0.0
        if len(boxes) > 0:
            crop_img = []
            for img_box in boxes:
                try:
                    crop_img.append(img.crop(img_box))
                except Exception as e:
                    logging.error(e, exc_info=True)
                    try:
                        crop_img.append(img)
                        crop_error += 0.1
                    except Exception as e:
                        logging.error(e, exc_info=True)
                        continue
        else:
            crop_error = 2
            crop_img = [img]

        if id2label is not None:
            labels = [id2label[x] for x in labels]

        img_array = asarray(img)
        for score, (xmin, ymin, xmax, ymax), label in zip(
            scores, boxes, labels
        ):
            if label == "license-plates":
                height, width, _ = img_array.shape
                # linewidth and thickness
                lw = max(
                    round(sum((height, width)) / 2 * 0.003), 2
                )  # Line width.
                tf = max(lw - 1, 1)  # Font thickness.
                cv2.rectangle(
                    img_array,
                    (int(xmin), int(ymin)),
                    (int(xmax), int(ymax)),
                    (0, 255, 0),
                    thickness=tf,
                )
                FONT_SCALE = 2e-3
                cv2.putText(
                    img=img_array,
                    text=f"{label}: {score:0.2f}",
                    org=(int(xmin), int(ymin)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=min(width, height) * FONT_SCALE,
                    color=(0, 255, 255),
                    thickness=tf,
                )

        license_located_img = Image.fromarray(img_array)
        if crop_error == 2:
            return license_located_img, license_located_img, crop_error
        return license_located_img, crop_img, crop_error

    def detect_objects(self, image_input, threshold):
        # Time process
        start_time_detection = time.perf_counter()

        # Make prediction
        processed_outputs = self.make_prediction(image_input)

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
