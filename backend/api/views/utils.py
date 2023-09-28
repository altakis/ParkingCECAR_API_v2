from detector_utils import detector_interface


def add_base64_objets_to_response(detection, options):
    return detector_interface.Detector.encode_base64_image_to_send_by_json(
        detection, options
    )


def get_base64_query_params(query_params):
    payload = {}

    try:
        pred_json_base64 = query_params.get("pred")
        if pred_json_base64:
            payload["pred_json_base64"] = pred_json_base64
    except Exception:
        pass

    try:
        crop_json_base64 = query_params.get("crop")
        if crop_json_base64:
            payload["crop_json_base64"] = crop_json_base64
    except Exception:
        pass

    return payload
