import os
from datetime import datetime
from pathlib import Path

from PIL import Image


class FileManagerUtil:
    _BASE_DIR = os.path.join(
        Path(__file__).resolve().parent.parent, "detection_imgs"
    )
    _img_folder = os.path.join(_BASE_DIR, "original")
    _crop_folder = os.path.join(_BASE_DIR, "crops")
    _tmp_folder = os.path.join(_BASE_DIR, "tmp")

    @property
    def BASE_DIR(self):
        return self._BASE_DIR

    @property
    def img_folder(self):
        return self._img_folder

    @property
    def crop_folder(self):
        return self._crop_folder

    @property
    def tmp_folder(self):
        return self._tmp_folder

    def __init__(self):
        self._folders = [
            self.BASE_DIR,
            self.img_folder,
            self.crop_folder,
            self.tmp_folder,
        ]

    def initialize_folders(self):
        for path in self._folders:
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)

    def save_img_results(
        self, img_visualization: Image.Image, img_crop: Image.Image
    ):
        now = datetime.now()
        dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")
        img_ori_name = f"{dt_string}_ori.png"
        img_crop_name = f"{dt_string}_crop.png"

        img_ori_loc = os.path.join(self._img_folder, img_ori_name)
        img_crop_loc = os.path.join(self._crop_folder, img_crop_name)

        img_visualization.save(img_ori_loc, "png")
        img_crop.save(img_crop_loc, "png")

        return img_ori_name, img_crop_name, img_ori_loc, img_crop_loc
