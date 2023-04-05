from fractions import Fraction
from itertools import chain
from time import time
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageDraw
from math import floor, ceil, pi, sin, cos
from collections import defaultdict
from random import randint, seed, random
from statistics import median
from werkzeug.utils import secure_filename
from uuid import uuid4

app = Flask(__name__)

BUILTIN_KERNELS = ['box', 'gauss', 'high-pass', 'low-pass', 'sobel']
UPLOAD_FOLDER = 'uploads/'

"""
Loads the image with the given filename and returns objects to 
allow image processing. 

:param filename: The filename of the image to load
:return: A tuple of (pixels, output_img, draw) where pixels is a
    2D array of pixels, output_img is a new image to draw on, and
    draw is an ImageDraw object to draw on output_img
"""
def load_img(filename):
    input_img = Image.open(filename)
    pixels = input_img.load()

    output_img = Image.new('RGB', (input_img.width, input_img.height))
    draw = ImageDraw.Draw(output_img)
    return pixels, output_img, draw

def new_load_img(filename):
    input_img = Image.open(filename)
    mode = input_img.mode
    pixels = input_img.load()
    output_img = Image.new(mode, (input_img.width, input_img.height))
    draw = ImageDraw.Draw(output_img)
    return input_img, pixels, output_img, draw


"""
Uploads an image to the server and returns the URL to the image
Renames the image to a UUID to prevent collisions
"""
@app.route('/upload', methods=['POST'])
def upload():
    # Check if no file was uploaded
    if 'file' not in request.files:
        return {'err': 'No file part'}
    
    file = request.files['file']
    if file.filename == '':
        return {'err': 'No selected file'}
    
    # Save and rename uploaded file
    if file:
        extension = file.filename.split('.')[-1]
        filename = f"{generate_filename()['filename']}.{extension}"
        path = UPLOAD_FOLDER + filename
        file.save(path)
        return {'url': path}

"""
Returns a given image from the upload folder
"""
@app.route(f'/{UPLOAD_FOLDER}<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


"""
Generates a randomized and secure filename for file uploads
"""
@app.route('/generate-filename')
def generate_filename():
    return {'filename': secure_filename(f'{uuid4().hex}')}


"""
Horizontally flips an image and returns the URL to the image
"""
@app.route('/horizontal-flip')
def horizontal_flip():
    # Load image
    pixels, output_img, draw = load_img('lenna.png')

    # Perform flip
    for x in range(output_img.width):
        for y in range(output_img.height):
            xp = output_img.width - x - 1
            draw.point((x, y), pixels[xp, y])

    # Save and return
    output_img.save('hflip.png')
    return 'Image flipped horizontally'


"""
Vertically flips an image and returns the URL to the image
"""
@app.route('/vertical-flip')
def vertical_flip():
    # Load image
    pixels, output_img, draw = load_img('lenna.png')

    # Perform flip
    for x in range(output_img.width):
        for y in range(output_img.height):
            yp = output_img.height - y - 1
            draw.point((x, y), pixels[x, yp])
    
    # Save and return
    output_img.save('vflip.png')
    return 'Image flipped vertically'

"""
Crops an image and returns the URL to the image
:param x: The x coordinate of the top left corner of the crop
:param y: The y coordinate of the top left corner of the crop
:param w: The width of the crop
:param h: The height of the crop
"""
@app.route('/crop')
def crop():
    # Get parameters from request
    topleft = (request.args.get('x', 0, int), request.args.get('y', 0, int))
    w, h = request.args.get('w', 1, int), request.args.get('h', 1, int)
    pixels, _, _ = load_img('lenna.png')
    mode = pixels.mode

    # Check if crop is valid
    if topleft[0] < 0 or topleft[1] < 0 or w < 0 or h < 0:
        return {'err': 'Invalid crop, all values must be positive'}
    if topleft[0] + w > pixels.width or topleft[1] + h > pixels.height:
        return {'err': 'Invalid crop, crop is out of bounds'}

    # Prepare output image
    output_img = Image.new(mode, (w, h))
    draw = ImageDraw.Draw(output_img)

    # Perform crop
    for x in range(output_img.width):
        for y in range(output_img.height):
            xp, yp = x + topleft[0], y + topleft[1]
            draw.point((x, y), pixels[xp, yp])
    
    # Save and return
    output_img.save(f'crop-x{topleft[0]}-y{topleft[1]}-w{w}-h{h}.png')
    return {'x': topleft[0], 'y': topleft[1], 'w': w, 'h': h, 'your-image': 'CROPPED'}


"""
Scales an image and returns the URL to the image
:param type: The type of scaling to use. Can be 'nn' for nearest neighbor
    or 'bl' for bilinear
:param w: The new width of the image
:param h: The new height of the image
"""
@app.route('/scale')
def scale():
    # Get parameters from request
    scale_type = request.args.get('type', 'nn', str)
    w, h = request.args.get('w', 1, int), request.args.get('h', 1, int)

    # Nearest neighbor scaling
    if scale_type == 'nn':
        # Load image
        pixels, _, _ = load_img('lenna.png')
        mode = pixels.mode

        # Prepare output image
        output_img = Image.new(mode, (w, h))
        draw = ImageDraw.Draw(output_img)

        # Determine scaling factors
        x_scale = pixels.width / w
        y_scale = pixels.height / h

        # Perform scaling
        for x in range(output_img.width):
            for y in range(output_img.height):
                xp, yp = floor(x * x_scale), floor(y * y_scale)
                draw.point((x, y), pixels[xp, yp])

        # Save and return
        output_img.save(f'scale-{scale_type}-w{w}-h{h}.png')
        return {'type': 'Nearest Neighbor', 'new-width': w, 'new-height': h}
    
    # Bilinear scaling
    elif scale_type == 'bl':
        # Load image
        pixels, _, _ = load_img('lenna.png')
        mode = pixels.mode
        num_channels = len(pixels.getbands())

        # Prepare output image
        output_img = Image.new(mode, (w, h))
        draw = ImageDraw.Draw(output_img)

        # Determine scaling factors
        x_scale = float(pixels.width - 1) / (w - 1) if w > 1 else 0
        y_scale = float(pixels.height - 1) / (h - 1) if h > 1 else 0

        # Perform scaling
        for x in range(output_img.width):
            for y in range(output_img.height):
                colour = [-1] * num_channels

                # Calculate bilinear interpolation for each channel
                for chan in range(num_channels):
                    xl, yl = floor(x * x_scale), floor(y * y_scale)
                    xh, yh = ceil(x * x_scale), ceil(y * y_scale)

                    xw = (x * x_scale) - xl
                    yw = (y * y_scale) - yl

                    a = pixels[xl, yl][chan]
                    b = pixels[xh, yl][chan]
                    c = pixels[xl, yh][chan]
                    d = pixels[xh, yh][chan]

                    colour[chan] = floor((a * (1 - xw) * (1 - yw)) + (b * xw * (1 - yw)) + (c * (1 - xw) * yw) + (d * xw * yw))

                # Set pixel colour after calculating interpolation for all channels
                draw.point((x,y), tuple(colour))

        # Save and return
        output_img.save(f'scale-{scale_type}-w{w}-h{h}.png')
        return {'type': 'Bilinear', 'new-width': w, 'new-height': h}

    # Bicubic scaling
    elif scale_type == 'bc':
        return {'type': 'Bicubic', 'err': 'Not implemented'}
    

"""
Rotates an image and returns the URL to the image
Images are cut off when rotated
:param deg: The angle to rotate the image by in degrees
"""
@app.route('/rotate')
def rotate():
    # Get parameters from request
    angle = (request.args.get('deg', 0, float) % 360.0) * (pi / 180)

    # Load image
    pixels, output_img, draw = load_img('lenna.png')
    cx, cy = output_img.width / 2, output_img.height / 2

    # Perform rotation
    for x in range(output_img.width):
        for y in range(output_img.height):
            # Calculate new pixel position based on given angle
            xp = (x - cx) * cos(angle) - (y - cy) * sin(angle) + cx
            yp = (x - cx) * sin(angle) + (y - cy) * cos(angle) + cy

            # Draw pixel if it is visible
            if 0 <= xp < output_img.width and 0 <= yp < output_img.height:
                draw.point((x, y), pixels[xp, yp])
    
    # Save and return
    output_img.save(f'rotate-{angle}rad.png')
    return {'rotation-rad': angle, 'rotation-deg': angle * (180 / pi)}

"""
Applies a linear or power map to an image and returns the URL to the image
:param type: The type of mapping to use. Can be 'linear' or 'power'
:param alpha: The alpha value for the linear map
:param beta: The beta value for the linear map
:param gamma: The gamma value for the power map
"""
@app.route('/map')
def grayscale_map():
    # Get parameters from request
    map_type = request.args.get('type')

    # Linear mapping
    if map_type == 'linear':
        # Get further parameters from request
        alpha = request.args.get('alpha', 1, float)
        beta = request.args.get('beta', 0, float)
        pixels, output_img, draw = load_img('lenna.png')

        # Perform mapping
        for x in range(output_img.width):
            for y in range(output_img.height):
                color = tuple([int((alpha * px) + beta) for px in pixels[x, y]])
                draw.point((x, y), color)

        # Save and return
        output_img.save(f'map-{map_type}-alpha{alpha}-beta{beta}.png')
        return {'mapping': map_type, 'alpha': alpha, 'beta': beta}
    
    # Power mapping
    elif map_type == 'power':
        # Get further parameters from request
        gamma = request.args.get('gamma', 1, float)
        L = 256 # TODO: make a dict of different image modes and their respective L values
        pixels, output_img, draw = load_img('lenna.png')

        # Perform mapping
        for x in range(output_img.width):
            for y in range(output_img.height):
                color = tuple([int((L - 1) * ((px / (L - 1)) ** gamma)) for px in pixels[x, y]])
                draw.point((x, y), color)

        # Save and return
        output_img.save(f'map-{map_type}-gamma{gamma}.png')
        return {'mapping': map_type, 'gamma': gamma}


"""
Calculates the histogram of an image and returns the histogram
"""
@app.route('/histogram')
# TODO: Add optional filename parameter so we can use this for equalization
def calculate_histogram():
    # Load image
    inimg, pixels, _, _ = new_load_img('jason.png')
    bands = inimg.getbands()
    channels = {band: defaultdict(int) for band in bands}

    # Calculate histogram by iterating over each pixel and band
    for x in range(inimg.width):
        for y in range(inimg.height):
            colour = pixels[x, y]
            for i, band in enumerate(bands):
                channels[band][colour[i]] += 1

    # Set default values for missing keys
    # TODO: Generalize this to work with any number bits
    for i in range(256):
        for band in bands:
            channels[band][i]

    return channels


"""
Calculates the histogram of the image and applies histogram equalization
:param eqalpha: Whether or not to equalize the alpha channel
"""
@app.route('/histogram-equalization')
def equalize_histogram():
    apply_to_alpha = request.args.get('apply-to-alpha', False, bool)

    # Load image
    channels = calculate_histogram() # TODO: Figure out how these will work together
    inimg, pixels, output_img, draw = new_load_img('jason.png')
    bands = inimg.getbands()
    nr_pixels = output_img.width * output_img.height

    # For each gray level, calculate new gray level
    new_graylevels = {band: calculate_new_gray_levels(channels.get(band), nr_pixels) for band in bands}

    # If alpha channel is not to be equalized, set it to the original value
    if not apply_to_alpha:
        try:
            if 'A' in bands:
                new_graylevels['A'] = {i : i for i in range(256)}
        except:
            pass

    # Apply equalization
    for x in range(output_img.width):
        for y in range(output_img.height):
            colour = pixels[x, y]
            print(colour)
            new_colour = tuple([new_graylevels[band][colour[i]] for i, band in enumerate(bands)])
            draw.point((x, y), new_colour)
    
    # Save and return
    output_img.save(f'equalized-jason.png')
    return new_graylevels


"""
Calculates the new gray levels for histogram equalization
:param graylevels: The histogram of the image
:param nr_pixels: The number of pixels in the image
"""
def calculate_new_gray_levels(graylevels : dict, nr_pixels: int): 
    # Calculate probability density function and cumulative distribution function
    pdf = {gl : nk / nr_pixels for gl, nk in graylevels.items()}
    pdf = {k: v for k, v in sorted(pdf.items(), key=lambda item: item[0])}
    cdf = {gl : sum([pdf[i] for i in range(gl + 1)]) for gl in pdf.keys()}
    
    # Calculate new gray levels and return
    return {gl : round((256 - 1) * cdf[gl]) for gl in cdf.keys()}


"""
Generates salt and pepper noise and returns the URL to the image
:param salt: The percentage chance of pixels to be set to white
:param pepper: The percentage chance of pixels to be set to black
:param noise_alpha: Whether or not to include the alpha channel in the noise
"""
@app.route('/generate-noise')
def generate_noise():
    # Get parameters from request and error check
    salt_chance, pepper_chance = request.args.get('salt', 5, float), request.args.get('pepper', 5, float)
    apply_to_alpha = request.args.get('apply-to-alpha', False, bool) # true if alpha channel should be included in noise

    if salt_chance > 100 or pepper_chance > 100 or salt_chance + pepper_chance > 100:
        return {'err': 'Salt and pepper values must be between 0 and 100'}

    # Load image and generate noise seed
    inimg, pixels, output_img, draw = new_load_img('dice.png')
    nr_bands = len(inimg.getbands())
    timeseed = int(time() * 1000)
    seed(timeseed)

    # Create salt and pepper colours
    if 'A' in inimg.getbands() and apply_to_alpha:
        salt = tuple([255] * (nr_bands - 1))
        pepper = tuple([0] * (nr_bands - 1))
    else:
        salt = tuple([255] * nr_bands)
        pepper = tuple([0] * nr_bands)

    # Generate salt and pepper based on chance
    for x in range(output_img.width):
        for y in range(output_img.height):
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
    output_img.save(f'noise-salt{salt_chance}-pepper{pepper_chance}-seed{timeseed}.png')
    return {'salt': salt_chance, 'pepper': pepper_chance, 'noise-alpha': apply_to_alpha, 'seed': timeseed}

# TOOD: Implement setting type of kernel (sobel, low pass etc.)
"""
Applies a kernel to an image and returns the URL to the image
:param kernel: The kernel to apply. Can either be a pre-defined kernel listed 
    in BUILTIN_KERNELS or a custom kernel. If it is a custom kernel, 
    it must be a rectangular matrix. This matrix can either be a 2D array of
    floats or of fractions. If it is a 2D array of fractions, the values will
    be converted to floats.
"""
@app.route('/kernel', methods=['POST'])
def kernel():
    # Check if there is data in the body
    try:
        data = request.get_json()
    except:
        return {'err': 'Empty request body'}

    # Check if data is valid
    apply_to_alpha = data.get('apply-to-alpha', False)
    kernel = data.get('kernel')
    if kernel is None:
        return {'err': 'Kernel not specified'}
    if kernel in BUILTIN_KERNELS:
        return {'kernel': kernel, 'err': 'Builtin kernels not implemented'}
    
    # Check that kernel is valid
    first_len = len(kernel[0])
    if not all(len(x) == first_len for x in kernel[1:]):
        return {'kernel': kernel, 'err': 'Kernel is not a rectangular matrix'}
    
    # If the values in the kernel aren't floats, convert them
    kernel = [[float(Fraction(i)) for i in j] for j in kernel]

    # Apply kernel
    inimg, pixels, output_img, draw = new_load_img('jason.png')
    bands = inimg.getbands()
    offset = len(kernel) // 2

    for x in range(offset, output_img.width - offset):
        for y in range(offset, output_img.height - offset):
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
    filename = f'kernel-{time()}.png'
    output_img.save(filename)
    return {'path': '/kernel', 'filename': filename, 'kernel': kernel}

"""
Applies a non-linear min, max or median filter to an image and returns the URL.
The filter can be a custom square size, but defaults to 3x3.
:param filter: The filter to apply. Can be either 'min', 'max' or 'median'
:param size: The size of the filter. Defaults to 3
"""
@app.route('/filter')
def filter():
    # Get parameters from request and error check
    filter_type = request.args.get('type')
    size = request.args.get('size', 3, int)
    apply_to_alpha = request.args.get('apply-to-alpha', False)

    # Load image
    inimg, pixels, output_img, draw = new_load_img('dice.png')
    bands = inimg.getbands()
    w, h = output_img.width, output_img.height

    # Error check parameters
    if filter_type not in ['min', 'max', 'median']:
        return {'type': filter, 'size': size, 'err': 'Invalid filter type'}

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
    output_img.save(f'filter-{filter_type}-{size}x{size}.png')
    return {'type': filter_type, 'size': size, 'apply-to-alpha': apply_to_alpha}


cors = CORS(app, resources={'/*':{'origins': 'http://localhost:3000'}}) 

if __name__ == "__main__":
    app.run()
