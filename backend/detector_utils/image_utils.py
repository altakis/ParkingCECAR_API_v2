import io

import cv2
import requests
import validators
from numpy import asarray, uint8
from numpy.typing import NDArray
from PIL import Image


def get_original_image(url_input):
    if validators.url(url_input):
        return Image.open(requests.get(url_input, stream=True).raw)


def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    pil_img = Image.open(buf)
    basewidth = 750
    wpercent = basewidth / float(pil_img.size[0])
    hsize = int((float(pil_img.size[1]) * float(wpercent)))

    return pil_img.resize((basewidth, hsize), Image.Resampling.LANCZOS)


def adjust_dimensions(img: Image.Image):
    # Get the current width and height
    width, height = img.size

    # Calculate the new width and height that are multiples of 32
    new_width = (width // 32) * 32
    new_height = (height // 32) * 32

    return img.resize((new_width, new_height))


def PIL2CV2(img: Image.Image):
    return cv2.cvtColor(asarray(img), cv2.COLOR_RGB2BGR)


def CV22PIL(imgOpenCV: NDArray[uint8]):
    return Image.fromarray(cv2.cvtColor(imgOpenCV, cv2.COLOR_BGR2RGB))
