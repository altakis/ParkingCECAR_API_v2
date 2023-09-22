import os
from datetime import datetime

from PIL import Image


class FileManagerUtil:
    def __init__(self):
        self._base_dir = os.path.join(os.getcwd(), "detection_imgs")
        self._img_folder = os.path.join(self._base_dir, "original")
        self._crop_folder = os.path.join(self._base_dir, "crops")
        self._folders = [self._base_dir, self._img_folder, self._crop_folder]

    def initialize_folders(self):
        for path in self._folders:
            #print(path)
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)

    def save_img_results(self, img_visualization: Image.Image, img_crop: Image.Image):
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
        img_ori_name = f"{dt_string}_ori.png"
        img_crop_name = f"{dt_string}_crop.png"

        img_ori_loc = os.path.join(self._img_folder, img_ori_name)
        img_crop_loc = os.path.join(self._crop_folder, img_crop_name)

        img_visualization.save(img_ori_loc, "png")
        img_crop.save(img_crop_loc, "png")

        return img_ori_name, img_crop_name, img_ori_loc, img_crop_loc
