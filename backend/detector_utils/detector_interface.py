import os

from PIL import Image

from . import base64_utils
from . import FileManagerUtil
from . import license_detector


class Detector:
    def __init__(self):
        # load license_detector
        detector_obj = license_detector.license_detector()
        self.detector = detector_obj

        # load fs utilities
        siu = FileManagerUtil.FileManagerUtil()
        self.save_img_util = siu

    def detect_license_from_fs_location(self, fs_location, options=None):
        # load data
        model_name = ""
        url_input = None
        image_input = None
        webcam_input = Image.open(fs_location)
        threshold = 0.5

        detection = self.detector.detect_objects(
            model_name, url_input, image_input, webcam_input, threshold
        )

        # save original file name
        # Normalize the path to use the appropriate path separator for the current OS
        normalized_path = os.path.normpath(fs_location)

        # Split the path to get the filename
        filename = os.path.basename(normalized_path)

        detection["file_name"] = filename

        # save img results
        self.save_img_util.initialize_folders()
        (
            img_ori_name,
            img_crop_name,
            img_ori_loc,
            img_crop_loc,
        ) = self.save_img_util.save_img_results(
            detection.get("viz_img"), detection.get("crop_img")
        )

        # Package according to data Detector model object
        current_record_name = detection.get("record_name")
        full_record_name = f"{current_record_name}{filename}"
        detection["record_name"] = full_record_name
        detection["pred_loc"] = img_ori_loc
        detection["crop_loc"] = img_crop_loc

        # Create base64 strings from detection
        pred_json_base64 = None
        crop_json_base64 = None
        if options:
            if options.get("pred_json_base64") == True:
                pred_json_base64 = base64_utils.encode(payload.get("pred_loc"))
            if options.get("crop_json_base64") == True:
                crop_json_base64 = base64_utils.encode(payload.get("crop_loc"))

        payload = {
            "detection": detection,
            "pred_json_base64": pred_json_base64,
            "crop_json_base64": crop_json_base64,
        }
        return payload

    def extract_file_name(image_path):
        # Normalize the path to use the appropriate path separator for the current OS
        normalized_path = os.path.normpath(path_string)

        # Split the path to get the filename
        filename = os.path.basename(normalized_path)

        return filename
