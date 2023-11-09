import datetime
import io
import logging
import time
from typing import List

import cv2
import easyocr
import numpy as np
import requests
import torch
import validators
from numpy import asarray
from PIL import Image
from transformers import (
    AutoFeatureExtractor,
    DetrForObjectDetection,
    YolosForObjectDetection,
)

# colors for visualization
from .constants import COLORS, MODELS, DEFAULT_MODEL


class LicenseOCRDetector:
    _models = MODELS
    _default_model = DEFAULT_MODEL

    def __init__(
        self, model="", gpu_available=False, ocr_verbose=False
    ) -> None:
        self._model = (
            LicenseOCRDetector._default_model if len(model) == 0 else model
        )
        self._reader = easyocr.Reader(
            ["en"], gpu=gpu_available, verbose=ocr_verbose
        )

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, model) -> None:
        if len(model) > 0:
            if model in LicenseOCRDetector._models:
                self._model = model
            else:
                self._model = LicenseOCRDetector._default_model
        return self.model

    def get_original_image(self, url_input):
        if validators.url(url_input):
            return Image.open(requests.get(url_input, stream=True).raw)

    def fig2img(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        pil_img = Image.open(buf)
        basewidth = 750
        wpercent = basewidth / float(pil_img.size[0])
        hsize = int((float(pil_img.size[1]) * float(wpercent)))
        return pil_img.resize((basewidth, hsize), Image.Resampling.LANCZOS)

    def make_prediction(self, img, feature_extractor, model):
        inputs = feature_extractor(img, return_tensors="pt")
        outputs = model(**inputs)
        img_size = torch.tensor([tuple(reversed(img.size))])
        processed_outputs = feature_extractor.post_process(outputs, img_size)
        return processed_outputs[0]

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

        img_array = np.array(img)
        for score, (xmin, ymin, xmax, ymax), label in zip(
            scores, boxes, labels
        ):
            if label == "license-plates":
                cv2.rectangle(
                    img_array,
                    (int(xmin), int(ymin)),
                    (int(xmax), int(ymax)),
                    (0, 255, 0),
                    thickness=10,
                )
                cv2.putText(
                    img=img_array,
                    text=f"{label}: {score:0.2f}",
                    org=(int(xmin), int(ymin)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=(0, 255, 255),
                    thickness=1,
                )

        license_located_img = Image.fromarray(img_array)
        if crop_error == 2:
            return license_located_img, license_located_img, crop_error
        return license_located_img, crop_img, crop_error

    def read_license_plate(self, license_plate_crop: Image.Image):
        # format PIL.Image input into grayscale
        license_plate_crop_gray = cv2.cvtColor(
            asarray(license_plate_crop), cv2.COLOR_BGR2GRAY
        )
        _, license_plate_crop_thresh = cv2.threshold(
            license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV
        )

        detections = self._reader.readtext(license_plate_crop_thresh)

        result = {}
        for index, detection in enumerate(detections):
            bbox, text, score = detection

            text = text.upper().strip()

            result[f"det_{index}"] = f"{text}_{score}"

        return result or None

    def get_ocr_output(self, crop_img_list: List[Image.Image], crop_error: int):
        start_time_ocr = time.perf_counter()

        # To prevent type errors with enumerate function below
        if type(crop_img_list) != List:
            crop_img_list = [crop_img_list]

        # OCR license plate
        license_text_ocr_result = {}
        for index, img in enumerate(crop_img_list):
            obj_index = f"obj_{index}"
            try:
                license_text_ocr_result[obj_index] = self.read_license_plate(
                    img
                )
            except Exception as e:
                logging.error(e, exc_info=True)
                license_text_ocr_result[obj_index] = f"Error: {e}"

        # Time out OCR
        ocr_process_time = time.perf_counter() - start_time_ocr

        return license_text_ocr_result, ocr_process_time

    def detect_objects(
        self, model_name, url_input, image_input, webcam_input, threshold
    ):
        # Time process
        start_time_detection = time.perf_counter()

        self.model = model_name

        # Extract model and feature extractor
        feature_extractor = AutoFeatureExtractor.from_pretrained(self.model)

        if "yolos" in self.model:
            model = YolosForObjectDetection.from_pretrained(self.model)
        elif "detr" in self.model:
            model = DetrForObjectDetection.from_pretrained(self.model)

        if validators.url(url_input):
            image = self.get_original_image(url_input)

        elif image_input:
            image = image_input

        elif webcam_input:
            image = webcam_input
            # 'flipping' the vertical axis of the input may be needed
            # depending on configuration of the webcam and emulator
            # see Gradio (https://www.gradio.app/docs/image)
            # specially regarding mirror_webcam attribute
            # image = image.transpose(Image.FLIP_LEFT_RIGHT)

        print("---"*5)
        print(image)
        print("---"*5)
        #image = image.convert("RGB")

        """ new_size = (640, 480)
        # Resize the image to the new size
        image = image.resize(new_size) """

        # Make prediction
        processed_outputs = self.make_prediction(
            image, feature_extractor, model
        )

        # Visualize prediction
        viz_img, crop_img, crop_error = self.visualize_prediction(
            image, processed_outputs, threshold, model.config.id2label
        )
        detection_process_time = time.perf_counter() - start_time_detection

        (
            license_text_ocr_result,
            ocr_process_time,
        ) = self.get_ocr_output(crop_img, crop_error)

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
