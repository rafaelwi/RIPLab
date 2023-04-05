# map.py
from PIL.Image import Image
from api.common import get_image_writables

def map(img : Image, params : dict) -> Image:
    """
    Maps a function to an image
    :param img: The image to map
    :param params: The parameters to map the image with. Must contain
    function key
    """
    pass
    # # Get parameters
    # function = params['function']

    # # Load image
    # pixels, new_img, draw = get_image_writables(img)

    # # Map image
    # for x in range(img.width):
    #     for y in range(img.height):
    #         color = tuple([function(px) for px in pixels[x, y]])
    #         draw.point((x, y), color)

    # # Save and return
    # return new_img


def linear_map(img : Image, params : dict) -> Image:
    """
    Maps a linear function to an image
    :param img: The image to map
    :param params: The parameters to map the image with. Must contain
    alpha and beta keys
    """
    # Get parameters
    alpha, beta = params['alpha'], params['beta']

    # Load image
    pixels, new_img, draw = get_image_writables(img)

    # Map image
    for x in range(img.width):
        for y in range(img.height):
            color = tuple([int((alpha * px) + beta) for px in pixels[x, y]])
            draw.point((x, y), color)

    # Save and return
    return new_img

def power_map(img : Image, params : dict) -> Image:
    """
    Maps a power function to an image
    :param img: The image to map
    :param params: The parameters to map the image with. Must contain
    gamma key
    """
    # Get parameters
    gamma = params['gamma']

    # Load image
    pixels, new_img, draw = get_image_writables(img)
    L = 256 # TODO: Get this from the image or make a dict with all the L values
            #       based on the image's mode

    # Map image
    for x in range(img.width):
        for y in range(img.height):
            color = tuple([int((L - 1) * ((px / (L - 1)) ** gamma)) for px in pixels[x, y]])
            draw.point((x, y), color)

    # Save and return
    return new_img
