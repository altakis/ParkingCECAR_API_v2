import datetime
import io
import time

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
COLORS = [
    [0.000, 0.447, 0.741],
    [0.850, 0.325, 0.098],
    [0.929, 0.694, 0.125],
    [0.494, 0.184, 0.556],
    [0.466, 0.674, 0.188],
    [0.301, 0.745, 0.933],
]


class license_detector:
    _models = [
        "nickmuchi/yolos-small-finetuned-license-plate-detection",
        "nickmuchi/detr-resnet50-license-plate-detection",
        "nickmuchi/yolos-small-rego-plates-detection",
    ]
    _default_model = "nickmuchi/yolos-small-finetuned-license-plate-detection"
    _reader = easyocr.Reader(["en"], gpu=False, verbose=False)

    def __init__(self, model="") -> None:
        if len(model) == 0:
            self._model = license_detector._default_model
        else:
            self._model = model

    def getCurrentModel(self) -> str:
        return self._model

    def setModelName(self, model) -> None:
        if model in license_detector._models:
            self._model = model
        else:
            self._model = license_detector._default_model

    def verifyModel(self, model):
        if len(model) == 0:
            self._model = license_detector._default_model
        else:
            self.setModelName(model)
        return self.getCurrentModel()

    def get_original_image(self, url_input):
        if validators.url(url_input):
            image = Image.open(requests.get(url_input, stream=True).raw)

            return image

    def fig2img(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        pil_img = Image.open(buf)
        basewidth = 750
        wpercent = basewidth / float(pil_img.size[0])
        hsize = int((float(pil_img.size[1]) * float(wpercent)))
        img = pil_img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
        return img

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
        crop_error = 0
        if len(boxes) > 0:
            try:
                crop_img = img.crop(*boxes)
            except:
                crop_error = 1
        else:
            crop_error = 2
            crop_img = img

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
        if crop_error > 0:
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

        for detection in detections:
            bbox, text, score = detection

            text = text.upper().strip()

            return text, score

        return None, None

    def get_ocr_output(self, crop_img: Image.Image, crop_error: int):
        start_time_ocr = time.perf_counter()

        # OCR license plate
        license_text, license_text_score = "", ""
        if crop_error == 0:
            license_text, license_text_score = self.read_license_plate(crop_img)
        else:
            license_text, license_text_score = "ERROR", 0

        # Time out OCR
        ocr_process_time = time.perf_counter() - start_time_ocr

        return license_text, license_text_score, ocr_process_time

    def detect_objects(
        self, model_name, url_input, image_input, webcam_input, threshold
    ):
        # Time process
        start_time_detection = time.perf_counter()

        model_name = self.verifyModel(model_name)

        # Extract model and feature extractor
        feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)

        if "yolos" in model_name:
            model = YolosForObjectDetection.from_pretrained(model_name)
        elif "detr" in model_name:
            model = DetrForObjectDetection.from_pretrained(model_name)

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
            license_text,
            license_text_score,
            ocr_process_time,
        ) = self.get_ocr_output(crop_img, crop_error)

        # package data and return
        time_stamp = datetime.datetime.now()
        data = {
            "record_name": f"{time_stamp}_",
            "time_stamp": time_stamp,
            "viz_img": viz_img,
            "crop_img": crop_img,
            "ocr_text_result": f"[ {license_text} ] : [{license_text_score}]",
            "processing_time_pred": round(detection_process_time, 20),
            "processing_time_ocr": round(ocr_process_time, 20),
        }

        return data
