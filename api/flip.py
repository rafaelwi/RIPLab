# flip.py
from PIL.Image import Image 
from api.common import get_image_writables

def horizontal_flip(img : Image) -> Image:
    """
    Flip an image horizontally
    :param img: The image to flip
    """
    # Load image
    pixels, new_img, draw = get_image_writables(img)

    # Flip image
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            xp = img.size[0] - x - 1
            draw.point((xp, y), pixels[x, y])

    # Save and return
    return new_img


def vertical_flip(img : Image) -> Image:
    """
    Flip an image vertically
    :param img: The image to flip
    """
    # Load image
    pixels, new_img, draw = get_image_writables(img)

    # Flip image
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            yp = img.size[1] - y - 1
            draw.point((x, yp), pixels[x, y])

    # Save and return
    return new_img
