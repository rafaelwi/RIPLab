# crop.py
from PIL.Image import Image
from common import get_image_pixels, get_new_image_writables

def crop(img: Image, params: dict) -> Image:
    """
    Crop an image
    :param img: The image to crop
    :param params: The parameters to crop the image with. Must 
    contain x, y, w, and h keys
    """
    # Get parameters
    topleft = (params['x'], params['y'])
    w, h = params['w'], params['h']

    # Load image and prepare output image
    pixels = get_image_pixels(img)
    new_img, draw = get_new_image_writables(w, h, img.mode)

    # Crop image
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            xp, yp =  x - topleft[0], y - topleft[1]
            draw.point((xp, yp), pixels[x, y])

    # Save and return
    return new_img
