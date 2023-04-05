# common.py
# Common functionality

from PIL import Image, ImageDraw


def get_image_writables(img : Image):
    """
    Get the pixels, mode, new image, and draw object for an image
    :param img: The image to get the writables for
    :return: The pixels, mode, new image, and draw object
    """
    pixels = img.load()
    mode = img.mode
    new_img = Image.new(mode, img.size)
    draw = ImageDraw.Draw(new_img)
    return pixels, new_img, draw


def get_new_image_writables(w : int, h : int, mode : str):
    """
    Create a new blank image and return its writables
    """
    new_img = Image.new(mode, (w, h))
    draw = ImageDraw.Draw(new_img)
    return new_img, draw


def get_image_pixels(img : Image):
    """
    Get the pixels for an image
    :param img: The image to get the pixels for
    :return: The pixels
    """
    return img.load()
