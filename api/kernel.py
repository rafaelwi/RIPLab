# kernel.py
from PIL.Image import Image
from common import get_image_writables

def kernel(img: Image, params: dict) -> Image:
    """
    Applies a kernel to an image and returns the URL to the image
    Data validation is done in the API, this assumes the kernel is valid
    :param kernel: The kernel to apply. Can either be a pre-defined kernel listed 
        in BUILTIN_KERNELS or a custom kernel. If it is a custom kernel, 
        it must be a rectangular matrix. This matrix can either be a 2D array of
        floats or of fractions. If it is a 2D array of fractions, the values will
        be converted to floats.
    """
    # Get parameters
    kernel = params['kernel']
    apply_to_alpha = params['apply_to_alpha']

    # Load image
    pixels, new_img, draw = get_image_writables(img)
    bands = img.getbands()
    offset = len(kernel) // 2

    # Apply kernel
    for x in range(offset, img.width - offset):
        for y in range(offset, img.height - offset):
            colour = [0] * len(bands)
            for a in range(len(kernel)):
                for b in range(len(kernel)):
                    xn = x + a - offset
                    yn = y + b - offset
                    pixel = pixels[xn, yn]
                    
                    # Apply to each channel
                    for i in range(len(bands)):
                        colour[i] += pixel[i] * kernel[a][b]

            # If we don't wan't to apply the kernel to the alpha channel, then
            # retrieve and replace the last value in the tuple with the original
            if 'A' in bands and not apply_to_alpha:
                colour = colour[:-1] + [pixels[x, y][-1]]

            # Draw the pixel
            final_colour = tuple([int(i) for i in colour])
            draw.point((x, y), final_colour)

    # Save and return
    return new_img
