# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-04-22 17:27:47
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Image methods.
"""


from typing import List, Union, Optional
from io import BytesIO
from os.path import abspath as os_abspath
from qrcode import make as qrcode_make
from PIL.Image import open as pil_open, LANCZOS

from .rsystem import rexc

try:
    from pyzbar.pyzbar import decode as pyzbar_decode
except:
    _, _, pyzbar_decode, _ = rexc.catch()


__all__ = (
    "encode_qrcode",
    "decode_qrcode",
    "compress_image"
)


def encode_qrcode(text: str, path: Optional[str] = None) -> Optional[bytes]:
    """
    `Encoding` text to `QR code` image.

    Parameters
    ----------
    text : Text.
    path : File generation path.
        - `None` : Not generate file, return image bytes data.
        - `str` : Save file, no return.

    Returns
    -------
    Image bytes data.
    """

    # Encode.
    image = qrcode_make(text)

    # Return.

    ## Save file and return file path.
    if path is not None:
        image.save(path)

    ## Return image bytes data.
    else:
        bytesio = BytesIO()
        image.save(bytesio)
        result = bytesio.getvalue()
        return result


def decode_qrcode(image: Union[str, bytes]) -> List[str]:
    """
    `Decoding` `QR code` or bar code image.

    Parameters
    ----------
    image : Image bytes data or image file path.

    Returns
    -------
    QR code or bar code text list.
    """

    # Check.
    if isinstance(pyzbar_decode, BaseException):
        raise pyzbar_decode

    # Handle parameter.
    if image.__class__ == bytes:
        image = BytesIO(image)

    # Decode.
    image = pil_open(image)
    qrcodes_data = pyzbar_decode(image)

    # Convert.
    texts = [
        data.data.decode()
        for data in qrcodes_data
    ]

    return texts


def compress_image(
    input_image: Union[str, bytes],
    ouput_image: Optional[str] = None,
    target_size: float = 0.5,
    rate: int = 5,
    reduce: bool = False,
    max_quality: int = 75,
    min_quality: int = 0
) -> Optional[bytes]:
    """
    `Compress` image file.

    Parameters
    ----------
    input_image : Input source image data.
        - `str` : Source image read file path.
        - `bytes` : Source image bytes data.

    output_image : Output compressed image data.
        - `None` : Return compressed image bytes data.
        - `str` : Compressed image file save path, no return.

    target_size : Compressed target size.
        - `value < 1` : Not more than this size ratio.
        - `value > 1` : Not more than this value, unit is KB.

    rate : Compressed iteration rate of quality and resolution.
    reduce : If target size is not completed, whether reduce image resolution for compression.
    max_quality : Iteration start image quality rate.
    min_quality : Iteration cutoff image quality rate.

    Returns
    -------
    Compressed image bytes data.
    """

    # Handle parameter.
    if input_image.__class__ == str:
        with open(input_image, "rb") as file:
            input_image = file.read()
    now_size = len(input_image)
    if target_size < 1:
        target_size = now_size * target_size
    else:
        target_size *= 1024

    # Read image.
    bytesio = BytesIO(input_image)
    image = pil_open(bytesio)
    image = image.convert("RGB")

    # Step compress.
    quality = max_quality
    while now_size > target_size and quality >= min_quality:
        bytesio = BytesIO()
        image.save(bytesio, "JPEG", quality=quality)
        now_size = len(bytesio.getvalue())
        quality -= rate

    # Step reduce.
    if reduce:
        ratio = 1 - rate / 100
        while now_size > target_size:
            bytesio = BytesIO()
            resize = image.size[0] * ratio, image.size[1] * ratio
            image.thumbnail(resize, LANCZOS)
            image.save(bytesio, "JPEG", quality=min_quality)
            now_size = len(bytesio.getvalue())
            ratio -= rate / 100

    # Return.
    content = bytesio.getvalue()

    ## return file bytes data.
    if ouput_image is None:
        return content

    ## Save file and return path.
    else:
        ouput_image = os_abspath(ouput_image)
        with open(ouput_image, "wb") as file:
            file.write(content)