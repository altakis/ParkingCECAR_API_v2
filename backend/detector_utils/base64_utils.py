import base64
from io import BytesIO
from typing import Union

from PIL import Image


def encode(source_image: Union[str, Image.Image]) -> str:
    if type(source_image) == str:
        # Open an image using Pillow
        image = Image.open(source_image)
    elif type(source_image) == Image.Image:
        image = source_image
    
    # Convert the PIL image to a binary stream (BytesIO)
    image_bytesio = BytesIO()
    image.save(
        image_bytesio, format="PNG"
    )  # You can specify the format you want (JPEG, PNG, etc.)

    # Get the binary data from the BytesIO stream
    image_binary = image_bytesio.getvalue()

    # Encode the binary data as Base64
    image_base64 = base64.b64encode(image_binary).decode(
        "utf-8"
    )  # Convert to a string

    return image_base64

def decode(source_image: str) -> Image.Image:
    # Decode the Base64 string to binary data
    image_binary = base64.b64decode(source_image.encode('utf-8'))

    # Create a BytesIO stream from the binary data
    image_bytesio = BytesIO(image_binary)

    # Open the image using Pillow
    image = Image.open(image_bytesio)

    return image


