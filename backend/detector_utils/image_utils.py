import io
from PIL import Image
import validators
import requests


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
