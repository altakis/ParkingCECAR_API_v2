import os
from datetime import datetime
from pathlib import Path
from typing import List, Union

from detector_utils.base64_utils import decode
from PIL import Image

from .constants import FOLDERS


class FileSystemInterface:
    _folder_list = FOLDERS
    _base_dir = FOLDERS["base_dir"]
    _img_folder = FOLDERS["img_folder"]
    _crop_folder = FOLDERS["crops_folder"]
    _tmp_folder = FOLDERS["tmp_folder"]

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
        for path in self.folder_list.values():
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
    def is_valid_file_path(file_path: Union[str, Path]) -> bool:
        if isinstance(file_path, str):
        # Check if it's a valid absolute file path
            if os.path.isabs(file_path) and os.path.exists(file_path):
                return True

            # Check if it can be converted to a Path object
            try:
                file_path = Path(file_path)
                return FileSystemInterface.check_if_Path_obj_is_exists(file_path)
            except (TypeError, ValueError):
                pass

        elif isinstance(file_path, Path):
            # Check if it's an absolute or relative Path object
            return FileSystemInterface.check_if_Path_obj_is_exists(file_path)

        return False

    @staticmethod
    def check_if_Path_obj_is_exists(file_path: Path) -> bool:
        return file_path.is_absolute() or file_path.exists()

    @staticmethod
    def save_img_to_folder(
        img: Image.Image, folder_path: str, file_name: str = None
    ) -> str:
        if file_name is not None:
            new_img_file_name = file_name
        else:            
            new_img_file_name = f"{FileSystemInterface.generate_timestamp_now()}_.png"

        save_path = os.path.join(folder_path, new_img_file_name)
        img.save(save_path, "png")
        return save_path

    @staticmethod
    def generate_timestamp_now():
        now = datetime.now()
        return now.strftime("%Y_%m_%d__%H_%M_%S")

    def save_base64_string_to_image_file_to_tmp_folder(
        self, base64_str: str, base64_file_name: str = None
    ) -> str:
        imported_img: Image.Image = decode(base64_str)
        if base64_file_name is not None:
            base64_file_name = f"{self.generate_timestamp_now()}_{base64_file_name}"
            return self.save_img_to_folder(
                imported_img, self.tmp_folder, base64_file_name
            )
        return self.save_img_to_folder(imported_img, self.tmp_folder)
