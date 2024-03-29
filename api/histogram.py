# histogram.py
from PIL.Image import Image
from common import get_image_pixels, get_image_writables
from collections import defaultdict

STROKE_COLOURS = {
    'R': '#ff0000',
    'G': '#00ff00',
    'B': '#0000ff',
    'L': '#808080',
    'A': '#c0c0c0',
    '1': '#000000'
}

def histogram(img : Image) -> tuple[dict, list, list]:
    """
    Get the histogram for an image
    :param img: The image to get the histogram for
    :return: The histogram
    """
    # Load image
    pixels = get_image_pixels(img)
    bands = img.getbands()
    channels = {band: defaultdict(int) for band in bands}
    channels_flat = []

    # Calculate histogram by iterating over each pixel and band
    if len(bands) == 1:
        for x in range(img.width):
            for y in range(img.height):
                colour = pixels[x, y]
                for i, band in enumerate(bands):
                    channels[band][colour] += 1
    else:
        for x in range(img.width):
            for y in range(img.height):
                colour = pixels[x, y]
                for i, band in enumerate(bands):
                    channels[band][colour[i]] += 1

    # Set default values for missing keys, and flatten histogram
    # TODO: Generalize this to work with any number bits
    for i in range(256):
        for band in bands:
            channels[band][i]
            channels_flat.append({
                'grayscale': i,
                band: channels[band][i]
            })

    # Create the series object for the histogram plot
    series = [{
                'xKey': 'grayscale', 
                'yKey': band, 
                'yName': band,
                'stroke': STROKE_COLOURS[band],
                'marker': {
                    'fill': STROKE_COLOURS[band],
                    'stroke': STROKE_COLOURS[band]
                }
            } for band in bands]

    # Return histogram
    return channels, channels_flat, series


def histogram_equalization(img : Image, params: dict) -> Image:
    """
    Perform histogram equalization on an image
    :param img: The image to perform histogram equalization on
    :param params: The parameters to perform histogram equalization with. Must
    contain the key 'channel'
    """
    # Get parameters
    apply_to_alpha = params['apply_to_alpha']

    # Load image
    channels, _, _ = histogram(img)
    pixels, new_img, draw = get_image_writables(img)
    bands = img.getbands()
    nr_pixels = img.width * img.height

    # For each gray level, calculate new gray level
    new_graylevels = {band: calculate_new_gray_levels(channels.get(band), nr_pixels) for band in bands}

    # If alpha channel is not to be equalized, set it to the original value
    if 'A' in bands and not apply_to_alpha:
        new_graylevels['A'] = {i : i for i in range(256)}

    # Apply equalization
    if len(bands) == 1:
        for x in range(img.width):
            for y in range(img.height):
                colour = pixels[x, y]
                new_colour = new_graylevels[bands[0]][colour]
                draw.point((x, y), new_colour)
    else:
        for x in range(img.width):
            for y in range(img.height):
                colour = pixels[x, y]
                new_colour = tuple([new_graylevels[band][colour[i]] for i, band in enumerate(bands)])
                draw.point((x, y), new_colour)

    return new_img


def calculate_new_gray_levels(graylevels : dict, nr_pixels: int): 
    """
    Calculates the new gray levels for histogram equalization
    :param graylevels: The histogram of the image
    :param nr_pixels: The number of pixels in the image
    """
    # Calculate probability density function and cumulative distribution function
    pdf = {gl : nk / nr_pixels for gl, nk in graylevels.items()}
    pdf = {k: v for k, v in sorted(pdf.items(), key=lambda item: item[0])}
    cdf = {gl : sum([pdf[i] for i in range(gl + 1)]) for gl in pdf.keys()}
    
    # Calculate new gray levels and return
    return {gl : round((256 - 1) * cdf[gl]) for gl in cdf.keys()}
