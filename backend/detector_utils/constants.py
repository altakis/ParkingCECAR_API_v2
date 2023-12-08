import os.path
from pathlib import Path


"""Constant file for the detector_utils module
"""
IMG_BASE_DIR = os.path.join(
    Path(__file__).resolve().parent.parent, "detection_imgs"
)
IMGS_FOLDER = os.path.join(IMG_BASE_DIR, "original")
CROPS_FOLDER = os.path.join(IMG_BASE_DIR, "crops")
TMP_FOLDER = os.path.join(IMG_BASE_DIR, "tmp")
FOLDERS = {
    "base_dir": IMG_BASE_DIR,
    "img_folder": IMGS_FOLDER,
    "crops_folder": CROPS_FOLDER,
    "tmp_folder": TMP_FOLDER,
}


# colors for visualization
COLORS = [
    [0.000, 0.447, 0.741],
    [0.850, 0.325, 0.098],
    [0.929, 0.694, 0.125],
    [0.494, 0.184, 0.556],
    [0.466, 0.674, 0.188],
    [0.301, 0.745, 0.933],
]
