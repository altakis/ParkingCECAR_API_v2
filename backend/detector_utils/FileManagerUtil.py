import os
from datetime import datetime
from pathlib import Path
from typing import List

from PIL import Image

from.constants import FOLDERS

class FileManagerUtil:
    _folder_list = FOLDERS
    _base_dir = FOLDERS[0]
    _img_folder = FOLDERS[1]
    _crop_folder = FOLDERS[2]
    _tmp_folder = FOLDERS[3]

    @property
    def BASE_DIR(self):
        return self._base_dir

    @property
    def img_folder(self):
        return self._img_folder

    @property
    def crop_folder(self):
        return self._crop_folder

    @property
    def tmp_folder(self):
        return self._tmp_folder

    @property
    def folder_list(self):
        return self._folder_list

    def __init__(self):
        self.initialize_folders()

    def initialize_folders(self):
        for path in self.folder_list:
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)

    def save_img_results(
        self, img_visualization: Image.Image, img_crop_list: List[Image.Image]
    ):
        now = datetime.now()
        dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")
        img_ori_name = f"{dt_string}_ori.png"
        img_ori_loc = os.path.join(self._img_folder, img_ori_name)
        img_visualization.save(img_ori_loc, "png")

        img_crop_name_list = []
        img_crop_loc_list = []

        # To prevent enumerate operation errors
        if isinstance(img_crop_list, Image.Image):
            img_crop_list = [img_crop_list]

        for index, crop in enumerate(img_crop_list):
            img_crop_name_list.append(f"{dt_string}_e{index}_crop.png")
            img_crop_loc_list.append(
                os.path.join(self._crop_folder, img_crop_name_list[index])
            )
            crop.save(img_crop_loc_list[index], "png")

        return img_ori_name, img_crop_name_list, img_ori_loc, img_crop_loc_list

    @staticmethod
    def is_valid_file_path(file_path):
        # Check for type of str
        if not type(file_path) == str:
            return False

        # Check if the path is an absolute path
        if not os.path.isabs(file_path):
            return False

        # Check if the path exists on the filesystem
        if not os.path.exists(file_path):
            return False

        # If both conditions are met, it's a valid file path
        return True