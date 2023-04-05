# rotate.py
from PIL.Image import Image
from common import get_image_writables
from math import pi, sin, cos

def rotate(img : Image, params : dict) -> Image:
    """
    Rotates an image and returns the URL to the image
    Images are cut off when rotated
    :param params: The parameters to scale the image with. Must contain deg key
    """

    # Get parameters
    angle = (params['deg'] % 360.0) * (pi / 180.0)

    # Load image
    pixels, new_img, draw = get_image_writables(img)
    cx, cy = img.width / 2, img.height / 2

    # Perform rotation
    for x in range(img.width):
        for y in range(img.height):
            # Calculate new pixel position based on given angle
            xp = (x - cx) * cos(angle) - (y - cy) * sin(angle) + cx
            yp = (x - cx) * sin(angle) + (y - cy) * cos(angle) + cy

            # Draw pixel if it is visible
            if 0 <= xp < img.width and 0 <= yp < img.height:
                draw.point((x, y), pixels[xp, yp])
    
    # Save and return
    return new_img
