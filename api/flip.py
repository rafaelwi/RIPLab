# flip.py
from PIL import Image 
from common import get_image_writables

def horizontal_flip(img : Image.Image) -> Image.Image:
    """
    Flip an image horizontally
    :param img: The image to flip
    """
    # Load image
    print('in horizontal_flip')
    pixels, new_img, draw = get_image_writables(img)

    # Flip image
    for x in range(img.width):
        for y in range(img.height):
            xp = img.width - x - 1
            draw.point((x, y), pixels[xp, y])

    # Save and return
    return new_img


def vertical_flip(img : Image.Image) -> Image.Image:
    """
    Flip an image vertically
    :param img: The image to flip
    """
    # Load image
    pixels, new_img, draw = get_image_writables(img)

    # Flip image
    for x in range(img.width):
        for y in range(img.height):
            yp = img.height - y - 1
            draw.point((x, y), pixels[x, yp])

    # Save and return
    return new_img
