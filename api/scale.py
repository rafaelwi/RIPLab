# scale.py
from PIL.Image import Image
from common import get_image_pixels, get_new_image_writables
from math import floor, ceil


def scale(img: Image, params: dict) -> Image:
    """
    Scales an image using the given scaling algorithm
    :param img: The image to scale
    :param params: The parameters to scale the image with. Must
    contain w, h, and type keys
    """
    if params['type'] == 'nn':
        return nearest_neighbour(img, params)
    elif params['type'] == 'bl':
        return bilinear(img, params)
    elif params['type'] == 'bc':
        return bicubic(img, params)


def nearest_neighbour(img: Image, params: dict) -> Image:
    """
    Scale an image using nearest neighbour scaling
    :param img: The image to scale
    :param params: The parameters to scale the image with. Must 
    contain w and h keys
    """
    # Get parameters
    w, h = params['w'], params['h']

    # Load image and prepare output image
    pixels = get_image_pixels(img)
    new_img, draw = get_new_image_writables(w, h, img.mode)

    # Determine scaling factors
    x_scale = img.size[0] / w
    y_scale = img.size[1] / h

    # Perform scaling
    for x in range(w):
        for y in range(h):
            xp, yp = floor(x * x_scale), floor(y * y_scale)
            draw.point((x, y), pixels[xp, yp])

    # Save and return
    return new_img


def bilinear(img: Image, params: dict) -> Image:
    """
    Scale an image using bilinear scaling
    :param img: The image to scale
    :param params: The parameters to scale the image with. Must 
    contain w and h keys
    """
    # Get parameters
    w, h = params['w'], params['h']

    # Load image and prepare output image
    pixels = get_image_pixels(img)
    nr_channels = len(img.getbands())
    new_img, draw = get_new_image_writables(w, h, img.mode)

    # Determine scaling factors
    x_scale = float(img.width - 1) / (w - 1) if w > 1 else 0
    y_scale = float(img.height - 1) / (h - 1) if h > 1 else 0

    # Perform scaling
    for x in range(w):
        for y in range(h):
            colour = [0] * nr_channels

            # Calculate bilinear interpolation for each channel
            for ch in range(nr_channels):
                xl, yl = floor(x * x_scale), floor(y * y_scale)
                xh, yh = ceil(x * x_scale), ceil(y * y_scale)

                xw = (x * x_scale) - xl
                yw = (y * y_scale) - yl

                a = pixels[xl, yl][ch]
                b = pixels[xh, yl][ch]
                c = pixels[xl, yh][ch]
                d = pixels[xh, yh][ch]

                colour[ch] = floor((a * (1 - xw) * (1 - yw)) + (b * xw * (1 - yw)) + (c * (1 - xw) * yw) + (d * xw * yw))
            draw.point((x, y), tuple(colour))
    
    # Save and return
    return new_img


def bicubic(img: Image, params: dict) -> Image:
    """
    **NOT IMPLEMENTED**
    
    Scale an image using bicubic scaling
    :param img: The image to scale
    :param params: The parameters to scale the image with. Must 
    contain w and h keys
    """
    return None
