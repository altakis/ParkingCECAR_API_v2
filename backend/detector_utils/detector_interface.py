import logging
import os

from PIL import Image

from . import FileManagerUtil, base64_utils, license_detector


class Detector:
    def __init__(self):
        # load license_detector
        detector_obj = license_detector.license_detector()
        self.detector = detector_obj

        # load fs utilities
        siu = FileManagerUtil.FileManagerUtil()
        self.save_img_util = siu

    def detect_license_from_fs_location(self, fs_location, options=None):
        check_path_validity = self.save_img_util.is_valid_file_path(fs_location)
        if not check_path_validity:
            return {}

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
        filename = self.extract_file_name(fs_location)

        detection["file_name"] = filename

        # create img folders if they don't exist
        self.save_img_util.initialize_folders()

        # save img results
        (
            img_ori_name,
            img_crop_name_list,
            img_ori_loc,
            img_crop_loc_list,
        ) = self.save_img_util.save_img_results(
            detection.get("viz_img"), detection.get("crop_img")
        )

        # Package according to data Detector model object
        current_record_name = detection.get("record_name")
        full_record_name = f"{current_record_name}{filename}"
        detection["record_name"] = full_record_name
        detection["pred_loc"] = img_ori_loc
        detection["crop_loc"] = " ".join(img_crop_loc_list)

        payload = {
            "detection": detection,
        }
        return payload

    @staticmethod
    def extract_file_name(image_path):
        # Normalize the path to use the appropriate path separator for the current OS
        normalized_path = os.path.normpath(image_path)

        # Split the path to get the filename
        filename = os.path.basename(normalized_path)

        return filename

    @staticmethod
    def encode_base64_image_to_send_by_json(detection, options):
        payload = {}
        payload["detection"] = detection

        # Create base64 strings from detection
        pred_json_base64 = None
        crop_json_base64 = None
        if options:
            if options.get("pred_json_base64") == True:
                pred_loc = detection.get("pred_loc")
                pred_json_base64 = base64_utils.encode(pred_loc)
                payload["pred_json_base64"] = pred_json_base64
                payload[
                    "pred_json_base64_filename"
                ] = Detector.extract_file_name(pred_loc)

            if options.get("crop_json_base64") == True:
                crop_loc = detection.get("crop_loc")
                crop_json_base64 = base64_utils.encode(crop_loc)
                payload["crop_json_base64"] = crop_json_base64
                payload[
                    "crop_json_base64_filename"
                ] = Detector.extract_file_name(crop_loc)

        return payload

    @staticmethod
    def check_for_base64_request_options(serializer_data, request_data):
        if len(request_data) > 0:
            return Detector.encode_base64_image_to_send_by_json(
                serializer_data, Detector.get_base64_query_params(request_data)
            )
        else:
            return serializer_data

    @staticmethod
    def get_base64_query_params(query_params):
        payload = {}

        try:
            pred_json_base64 = query_params.get("pred")
            if pred_json_base64:
                payload["pred_json_base64"] = pred_json_base64
        except Exception as e:
            logging.info(e, exc_info=True)
            pass

        try:
            crop_json_base64 = query_params.get("crop")
            if crop_json_base64:
                payload["crop_json_base64"] = crop_json_base64
        except Exception as e:
            logging.info(e, exc_info=True)
            pass

        return payload
