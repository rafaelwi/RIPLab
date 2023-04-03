from fractions import Fraction
from itertools import chain
from time import time
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageDraw
from math import floor, ceil, pi, sin, cos
from collections import defaultdict
from random import seed, random
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


"""
Uploads an image to the server and returns the URL to the image
Renames the image to a UUID to prevent collisions
"""
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return {'err': 'No file part'}
    file = request.files['file']
    if file.filename == '':
        return {'err': 'No selected file'}
    if file:
        extension = file.filename.split('.')[-1]
        filename = UPLOAD_FOLDER + secure_filename(f'{uuid4().hex}.{extension}')
        file.save(filename)
        return {'url': filename}

"""
Returns a given image from the upload folder
"""
@app.route(f'/{UPLOAD_FOLDER}<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# TOOD: Generate filenames

"""
Horizontally flips an image and returns the URL to the image
"""
@app.route('/horizontal-flip')
def horizontal_flip():
    pixels, output_img, draw = load_img('lenna.png')

    for x in range(output_img.width):
        for y in range(output_img.height):
            xp = output_img.width - x - 1
            draw.point((x, y), pixels[xp, y])

    output_img.save('hflip.png')
    return 'Image flipped horizontally'


"""
Vertically flips an image and returns the URL to the image
"""
@app.route('/vertical-flip')
def vertical_flip():
    pixels, output_img, draw = load_img('lenna.png')

    for x in range(output_img.width):
        for y in range(output_img.height):
            yp = output_img.height - y - 1
            draw.point((x, y), pixels[x, yp])
    
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
    topleft = (request.args.get('x', 0, int), request.args.get('y', 0, int))
    w, h = request.args.get('w', 1, int), request.args.get('h', 1, int)
    pixels, _, _ = load_img('lenna.png')

    # TODO: Generalize for any image type
    # TODO: Check if crop is valid
    output_img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(output_img)

    for x in range(output_img.width):
        for y in range(output_img.height):
            xp, yp = x + topleft[0], y + topleft[1]
            draw.point((x, y), pixels[xp, yp])
    
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
    scale_type = request.args.get('type', 'nn', str)
    w, h = request.args.get('w', 1, int), request.args.get('h', 1, int)

    if scale_type == 'nn':
        pixels, _, _ = load_img('lenna.png')
        output_img = Image.new('RGB', (w, h))
        draw = ImageDraw.Draw(output_img)

        x_scale = 512 / w
        y_scale = 512 / h

        for x in range(output_img.width):
            for y in range(output_img.height):
                xp, yp = floor(x * x_scale), floor(y * y_scale)
                draw.point((x, y), pixels[xp, yp])

        output_img.save(f'scale-{scale_type}-w{w}-h{h}.png')
        return {'type': 'Nearest Neighbor', 'new-width': w, 'new-height': h}
    elif scale_type == 'bl':
        pixels, _, _ = load_img('lenna.png')
        output_img = Image.new('RGB', (w, h))
        draw = ImageDraw.Draw(output_img)

        x_scale = float(512 - 1) / (w - 1) if w > 1 else 0
        y_scale = float(512 - 1) / (h - 1) if h > 1 else 0

        for x in range(output_img.width):
            for y in range(output_img.height):
                rgb = [-1, -1, -1, -1]

                for chan in range(3): # loop through RGB channels
                    xl, yl = floor(x * x_scale), floor(y * y_scale)
                    xh, yh = ceil(x * x_scale), ceil(y * y_scale)

                    xw = (x * x_scale) - xl
                    yw = (y * y_scale) - yl

                    a = pixels[xl, yl][chan]
                    b = pixels[xh, yl][chan]
                    c = pixels[xl, yh][chan]
                    d = pixels[xh, yh][chan]

                    rgb[chan] = floor((a * (1 - xw) * (1 - yw)) + (b * xw * (1 - yw)) + (c * (1 - xw) * yw) + (d * xw * yw))
                draw.point((x,y), tuple(rgb))

        output_img.save(f'scale-{scale_type}-w{w}-h{h}.png')
        return {'type': 'Bilinear', 'new-width': w, 'new-height': h}
    elif scale_type == 'bc':
        return {'type': 'Bicubic', 'err': 'Not implemented'}
    

"""
Rotates an image and returns the URL to the image
Images are cut off when rotated
:param deg: The angle to rotate the image by in degrees
"""
@app.route('/rotate')
def rotate():
    angle = (request.args.get('deg', 0, float) % 360.0) * (pi / 180)
    pixels, output_img, draw = load_img('lenna.png')
    cx, cy = output_img.width / 2, output_img.height / 2

    for x in range(output_img.width):
        for y in range(output_img.height):
            xp = (x - cx) * cos(angle) - (y - cy) * sin(angle) + cx
            yp = (x - cx) * sin(angle) + (y - cy) * cos(angle) + cy

            if 0 <= xp < output_img.width and 0 <= yp < output_img.height:
                draw.point((x, y), pixels[xp, yp])
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
    map_type = request.args.get('type')

    if map_type == 'linear':
        alpha = request.args.get('alpha', 1, float)
        beta = request.args.get('beta', 0, float)
        pixels, output_img, draw = load_img('lenna.png')

        for x in range(output_img.width):
            for y in range(output_img.height):
                color = tuple([int((alpha * px) + beta) for px in pixels[x, y]])
                draw.point((x, y), color)

        output_img.save(f'map-{map_type}-alpha{alpha}-beta{beta}.png')
        return {'mapping': map_type, 'alpha': alpha, 'beta': beta}
    elif map_type == 'power':
        gamma = request.args.get('gamma', 1, float)
        L = 256 # TODO: get from image
        pixels, output_img, draw = load_img('lenna.png')

        for x in range(output_img.width):
            for y in range(output_img.height):
                color = tuple([int((L - 1) * ((px / (L - 1)) ** gamma)) for px in pixels[x, y]])
                draw.point((x, y), color)
        output_img.save(f'map-{map_type}-gamma{gamma}.png')
        return {'mapping': map_type, 'gamma': gamma}


"""
Calculates the histogram of an image and returns the histogram
"""
@app.route('/histogram')
def calculate_histogram():
    reds, greens, blues = defaultdict(int), defaultdict(int), defaultdict(int)
    pixels, img, _ = load_img('lenna.png')

    # TODO: Generalize this to work with any number of channels
    for x in range(img.width):
        for y in range(img.height):
            r, g, b = pixels[x, y]
            reds[r] += 1
            greens[g] += 1
            blues[b] += 1

    # Set default values for missing keys
    for i in range(256):
        reds[i]
        greens[i]
        blues[i]

    return {'red': reds, 'green': greens, 'blue': blues}

"""
Calculates the histogram of the image and applies histogram equalization
"""
@app.route('/histogram-equalization')
def equalize_histogram():
    reds, greens, blues = calculate_histogram().values() # TODO: Figure out how these will work together
    pixels, output_img, draw = load_img('lenna.png')
    nr_pixels = output_img.width * output_img.height

    # TODO: Generalize this to work with any number of channels
    # For each gray level, calculate new gray level
    nr = calculate_new_gray_levels(reds, nr_pixels)
    ng = calculate_new_gray_levels(greens, nr_pixels)
    nb = calculate_new_gray_levels(blues, nr_pixels)

    # Apply
    for x in range(output_img.width):
        for y in range(output_img.height):
            r, g, b = pixels[x, y]
            draw.point((x, y), (nr[r], ng[g], nb[b]))
    
    output_img.save(f'equalized.png')
    return {'red': nr, 'green': ng, 'blue': nb}


"""
Calculates the new gray levels for histogram equalization
:param graylevels: The histogram of the image
:param nr_pixels: The number of pixels in the image
"""
def calculate_new_gray_levels(graylevels : dict, nr_pixels: int): 
    pdf = {gl : nk / nr_pixels for gl, nk in graylevels.items()}
    pdf = {k: v for k, v in sorted(pdf.items(), key=lambda item: item[0])}
    cdf = {gl : sum([pdf[i] for i in range(gl + 1)]) for gl in pdf.keys()}
    return {gl : round((256 - 1) * cdf[gl]) for gl in cdf.keys()}


"""
Generates salt and pepper noise and returns the URL to the image
:param salt: The percentage chance of pixels to be set to white
:param pepper: The percentage chance of pixels to be set to black
"""
@app.route('/generate-noise')
def generate_noise():
    salt, pepper = request.args.get('salt', 5, float), request.args.get('pepper', 5, float)
    if salt > 100 or pepper > 100 or salt + pepper > 100:
        return {'err': 'Salt and pepper values must be between 0 and 100'}

    pixels, output_img, draw = load_img('lenna.png')
    timeseed = int(time() * 1000)
    seed(timeseed)

    # TODO: Generalize this to work with any number of channels
    for x in range(output_img.width):
        for y in range(output_img.height):
            if random() < salt / 100:
                draw.point((x, y), (255, 255, 255))
            elif random() < pepper / 100:
                draw.point((x, y), (0, 0, 0))
            else:
                draw.point((x, y), pixels[x, y])
    output_img.save(f'noise-salt{salt}-pepper{pepper}-seed{timeseed}.png')

    return {'salt': salt, 'pepper': pepper, 'seed': timeseed}

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
    try:
        data = request.get_json()
    except:
        return {'err': 'Empty request body'}

    # Check if data is valid
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

    # TODO: Generalize this to work with any number of channels
    pixels, output_img, draw = load_img('lenna.png')
    offset = len(kernel) // 2
    for x in range(offset, output_img.width - offset):
        for y in range(offset, output_img.height - offset):
            colour = [0, 0, 0]
            for a in range(len(kernel)):
                for b in range(len(kernel)):
                    xn = x + a - offset
                    yn = y + b - offset
                    pixel = pixels[xn, yn]
                    colour[0] += pixel[0] * kernel[a][b]
                    colour[1] += pixel[1] * kernel[a][b]
                    colour[2] += pixel[2] * kernel[a][b]
            draw.point((x, y), (int(colour[0]), int(colour[1]), int(colour[2])))
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
    filter_type = request.args.get('type')
    size = request.args.get('size', 3, int)

    pixels, output_img, draw = load_img('lenna.png')
    w, h = output_img.width, output_img.height

    if filter_type not in ['min', 'max', 'median']:
        return {'type': filter, 'size': size, 'err': 'Invalid filter type'}

    # Get a chunk of the image
    chunk = list()
    for x in range (w - size + 1):
        for y in range (h - size + 1):
            chunk = [pixels[x+a, y+b] for a in range(size) for b in range(size)]
            reds = [i[0] for i in chunk]
            greens = [i[1] for i in chunk]
            blues = [i[2] for i in chunk]

            # TODO: Generalize this to work with any number of channels
            if filter_type == 'min':
                colour = (min(reds), min(greens), min(blues))
            elif filter_type == 'max':
                colour = (max(reds), max(greens), max(blues))
            elif filter_type == 'median':
                colour = (median(reds), median(greens), median(blues))

            draw.point((x,y), colour)
    output_img.save(f'filter-{filter_type}-{size}x{size}.png')
    return {'type': filter_type, 'size': size}


cors = CORS(app, resources={'/*':{'origins': 'http://localhost:3000'}}) 

if __name__ == "__main__":
    app.run()
