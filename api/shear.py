# shear.py
from PIL.Image import Image
from common import get_new_image_writables, get_image_pixels
from math import tan, pi


def shear(img : Image, params : dict) -> Image:
    """
    Shears an image in a given direction by a given angle.
    :param img: The image to shear.
    :param params: A dictionary containing the parameters for the shear.
    """
    if params['direction'] == 'vertical':
        return vertical_sheer(img, params)
    elif params['direction'] == 'horizontal':
        return horizontal_sheer(img, params)
    

def vertical_sheer(img : Image, params : dict) -> Image:
    """
    Vertically shears an image by a given angle.
    :param img: The image to shear.
    :param params: A dictionary containing the parameters for the shear.
    """
    # Get parameters
    angle = params['deg'] * (pi / 180.0)
    shear_factor = -tan(angle)

    # Create a new image and load image to shear
    mode = img.mode
    shear_width = img.width + (int(abs(shear_factor) * img.height))
    shear_height = img.height
    new_img, draw = get_new_image_writables(shear_width, shear_height, mode)
    pixels = get_image_pixels(img)

    # Perform shear
    for x in range(shear_width):
        for y in range(shear_height):
            # Calculate the corresponding pixel in the original image
            if angle < 0:
                x_original = int((x - (shear_width - img.width) / 2) - abs(shear_factor) * (y - (shear_height / 2)))
            else:
                x_original = int((x - (shear_width - img.width) / 2) - shear_factor * (y - (shear_height / 2)))
            y_original = y

            # Check if the pixel is within the bounds of the original image
            if 0 <= x_original < img.width and 0 <= y_original < img.height:
                colour = pixels[x_original, y_original]
                draw.point((x, y), colour)

    # Save and return
    return new_img


def horizontal_sheer(img : Image, params : dict) -> Image:
    """
    Horizontally shears an image by a given angle.
    :param img: The image to shear.
    :param params: A dictionary containing the parameters for the shear.
    """
    # Get parameters
    angle = params['deg'] * (pi / 180.0)
    shear_factor = -tan(angle)

    # Create a new image and load image to shear
    mode = img.mode
    shear_width = img.width
    shear_height = img.height + (int(abs(shear_factor) * img.width))
    new_img, draw = get_new_image_writables(shear_width, shear_height, mode)
    pixels = get_image_pixels(img)

    # Perform shear
    for x in range(shear_width):
        for y in range(shear_height):
            # Calculate the corresponding pixel in the original image
            if angle < 0:
                y_original = int((x - (shear_height - img.height) / 2) - abs(shear_factor) * (y - (shear_width / 2)))
            else:
                y_original = int((x - (shear_height - img.height) / 2) - shear_factor * (y - (shear_width / 2)))
            x_original = x

            # Check if the pixel is within the bounds of the original image
            if 0 <= x_original < img.width and 0 <= y_original < img.height:
                colour = pixels[x_original, y_original]
                draw.point((x, y), colour)

    # Save and return
    return new_img
