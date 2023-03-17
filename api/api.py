import time
from flask import Flask, request
from flask_cors import CORS
from PIL import Image, ImageDraw
from math import floor, ceil, pi, sin, cos
from collections import defaultdict

app = Flask(__name__)

def load_img(filename):
    input_img = Image.open(filename)
    pixels = input_img.load()

    output_img = Image.new('RGB', (input_img.width, input_img.height))
    draw = ImageDraw.Draw(output_img)
    return pixels, output_img, draw

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/horizontal-flip')
def horizontal_flip():
    pixels, output_img, draw = load_img('lenna.png')

    for x in range(output_img.width):
        for y in range(output_img.height):
            xp = output_img.width - x - 1
            draw.point((x, y), pixels[xp, y])

    output_img.save('hflip.png')
    return 'Image flipped horizontally'

@app.route('/vertical-flip')
def vertical_flip():
    pixels, output_img, draw = load_img('lenna.png')

    for x in range(output_img.width):
        for y in range(output_img.height):
            yp = output_img.height - y - 1
            draw.point((x, y), pixels[x, yp])
    
    output_img.save('vflip.png')
    return 'Image flipped vertically'

@app.route('/crop')
def crop():
    topleft = (int(request.args.get('x')), int(request.args.get('y')))
    w, h = int(request.args.get('w')), int(request.args.get('h'))
    pixels, _, _ = load_img('lenna.png')

    output_img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(output_img)

    for x in range(output_img.width):
        for y in range(output_img.height):
            xp, yp = x + topleft[0], y + topleft[1]
            draw.point((x, y), pixels[xp, yp])
    
    output_img.save(f'crop-x{topleft[0]}-y{topleft[1]}-w{w}-h{h}.png')
    return {'x': topleft[0], 'y': topleft[1], 'w': w, 'h': h, 'your-image': 'CROPPED'}

@app.route('/scale')
def scale():
    scale_type = request.args.get('type')
    w, h = int(request.args.get('w')), int(request.args.get('h'))

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
    
@app.route('/rotate')
def rotate():
    angle = (float(request.args.get('deg')) % 360.0) * (pi / 180)
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

@app.route('/map')
def grayscale_map():
    map_type = request.args.get('type')

    if map_type == 'linear':
        alpha = request.args.get('alpha', 1, float)
        beta = request.args.get('beta', 0, float)
        pixels, output_img, draw = load_img('lenna.png')

        for x in range(output_img.width):
            for y in range(output_img.height):
                color = tuple([int((alpha * px) + beta) for px in pixels[x, y] ])
                draw.point((x, y), color)

        output_img.save(f'map-{map_type}-alpha{alpha}-beta{beta}.png')
        return {'mapping': map_type, 'alpha': alpha, 'beta': beta}
    elif map_type == 'power':
        gamma = request.args.get('gamma', 1, float)
        L = 256 # TODO: get from image
        pixels, output_img, draw = load_img('lenna.png')

        for x in range(output_img.width):
            for y in range(output_img.height):
                color = tuple([int((L - 1) * ((px / (L - 1)) ** gamma)) for px in pixels[x, y] ])
                draw.point((x, y), color)
        output_img.save(f'map-{map_type}-gamma{gamma}.png')
        return {'mapping': map_type, 'gamma': gamma}
    
@app.route('/histogram')
def calculate_histogram():
    reds, greens, blues = defaultdict(int), defaultdict(int), defaultdict(int)
    pixels, img, _ = load_img('lenna.png')

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

@app.route('/histogram-equalization')
def equalize_histogram():
    reds, greens, blues = calculate_histogram().values() # TODO: Figure out how these will work together
    
    pixels, output_img, draw = load_img('lenna.png')
    nr_pixels = output_img.width * output_img.height

    # For each gray level, calculate PDF
    reds_pdf = calculate_pdf(reds, nr_pixels)
    greens_pdf = calculate_pdf(greens, nr_pixels)
    blues_pdf = calculate_pdf(blues, nr_pixels)

    # For each gray level, calculate CDF
    reds_cdf = calculate_cdf(reds_pdf)
    greens_cdf = calculate_cdf(greens_pdf)
    blues_cdf = calculate_cdf(blues_pdf)

    # For each gray level, calculate new gray level
    nr = calculate_new_gray_levels(reds_cdf)
    ng = calculate_new_gray_levels(greens_cdf)
    nb = calculate_new_gray_levels(blues_cdf)

    # Apply
    for x in range(output_img.width):
        for y in range(output_img.height):
            r, g, b = pixels[x, y]
            draw.point((x, y), (nr[r], ng[g], nb[b]))
    
    output_img.save(f'equalized.png')
    return {'red': nr, 'green': ng, 'blue': nb}

def calculate_pdf(graylevels : dict, nr_pixels: int): # sort them too
    pdf =  {gl : nk / nr_pixels for gl, nk in graylevels.items()}
    # sort and return the pdf by key
    return {k: v for k, v in sorted(pdf.items(), key=lambda item: item[0])}

def calculate_cdf(pdf : dict):
    return {gl : sum([pdf[i] for i in range(gl + 1)]) for gl in pdf.keys()}

def calculate_new_gray_levels(cdf : dict):
    return {gl : round((256 - 1) * cdf[gl]) for gl in cdf.keys()}


cors = CORS(app, resources={'/*':{'origins': 'http://localhost:3000'}}) 

if __name__ == "__main__":
    app.run()
