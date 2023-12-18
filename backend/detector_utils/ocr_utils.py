import logging
import time
from typing import List

import cv2
from numpy import asarray, uint8
from numpy.typing import NDArray
from PIL import Image


def read_license_plate(ocr_reader, license_plate_crop: NDArray[uint8]):
    # format PIL.Image input into grayscale
    license_plate_crop_gray = cv2.cvtColor(
        asarray(license_plate_crop), cv2.COLOR_BGR2GRAY
    )
    _, license_plate_crop_thresh = cv2.threshold(
        license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV
    )

    detections = ocr_reader.readtext(license_plate_crop_thresh)

    result = {}
    for index, detection in enumerate(detections):
        bbox, text, score = detection

        text = text.upper().strip()

        result[f"dt_{index}"] = f"{text}_{score:.4}"

    return result or None


def get_ocr_output(
    ocr_reader, crop_img_list: List[Image.Image], crop_error: int
):
    start_time_ocr = time.perf_counter()

    # OCR license plate
    license_text_ocr_result = {}
    for index, img in enumerate(crop_img_list):
        obj_index = f"r_{index}"
        try:
            """# Experimental size scaling for more accurate ocr
            width, height = img.size
            new_size = (int(width * 1.5), int(height * 1.5))
            img = img.resize(new_size)"""
            license_text_ocr_result[obj_index] = read_license_plate(
                ocr_reader, img
            )
        except Exception as e:
            logging.error(e, exc_info=True)
            license_text_ocr_result[obj_index] = f"Error: {e}"

    # Time out OCR
    ocr_process_time = time.perf_counter() - start_time_ocr

    return license_text_ocr_result, ocr_process_time
