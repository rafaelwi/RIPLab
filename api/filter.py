# filter.py
from random import randint, random, seed
from statistics import median
from PIL.Image import Image
from common import get_image_writables
from time import time

def generate_noise(img: Image, params: dict) -> Image:
    """
    Generates salt and pepper noise and returns the URL to the image
    :param salt: The percentage chance of pixels to be set to white
    :param pepper: The percentage chance of pixels to be set to black
    :param apply_to_alpha: Whether or not to include the alpha channel in the noise
    """

    # Get parameters
    salt_chance, pepper_chance = params['salt_chance'], params['pepper_chance']
    apply_to_alpha = params['apply_to_alpha']

    # Load image and generate noise seed
    pixels, new_img, draw = get_image_writables(img)
    nr_bands = len(img.getbands())
    timeseed = int(time())
    seed(timeseed)

    # Create salt and pepper colours
    if 'A' in img.getbands() and apply_to_alpha:
        salt = tuple([255] * (nr_bands - 1))
        pepper = tuple([0] * (nr_bands - 1))
    else:
        salt = tuple([255] * nr_bands)
        pepper = tuple([0] * (nr_bands - 1) + [255])

        # Generate salt and pepper based on chance
    for x in range(img.width):
        for y in range(img.height):
            # Determine chance of changing pixel and chance of salt or pepper
            random_num = random()
            random_type = randint(0, 1)

            # Salting
            if random_type == 0:
                if random_num < salt_chance / 100 and apply_to_alpha:
                    draw.point((x, y), salt + (pixels[x, y][-1],))
                elif random_num < salt_chance / 100:
                    draw.point((x, y), salt)
                else:
                    draw.point((x, y), pixels[x, y])
            
            # Peppering
            else:
                if random_num < pepper_chance / 100 and apply_to_alpha:
                    draw.point((x, y), pepper + (pixels[x, y][-1],))
                elif random_num < pepper_chance / 100:
                    draw.point((x, y), pepper)
                else:
                    draw.point((x, y), pixels[x, y])
    
    # Save and return
    return new_img

def filter(img: Image, params: dict):
    """
    Applies a non-linear min, max or median filter to an image and returns the URL.
    The filter can be a custom square size, but defaults to 3x3.
    :param filter: The filter to apply. Can be either 'min', 'max' or 'median'
    :param size: The size of the filter. Defaults to 3
    """
    # Get parameters
    filter_type = params['type']
    size = params['size']
    apply_to_alpha = params['apply_to_alpha']

    # Load image
    pixels, new_img, draw = get_image_writables(img)
    bands = img.getbands()
    w, h = img.size

    # Get a chunk of the image
    chunk = list()
    for x in range (w - size + 1):
        for y in range (h - size + 1):
            chunk = [pixels[x+a, y+b] for a in range(size) for b in range(size)]
            colours = list(zip(*chunk))

            # Apply filter
            if filter_type == 'min':
                colour = tuple([min(i) for i in colours])
            elif filter_type == 'max':
                colour = tuple([max(i) for i in colours])
            elif filter_type == 'median':
                colour = tuple([median(i) for i in colours])

            # Check if we need to apply the filter to the alpha channel
            if 'A' in bands and not apply_to_alpha:
                colour = colour[:-1] + (pixels[x, y][-1],)

            draw.point((x,y), colour)
    
    # Save and return
    return new_img
