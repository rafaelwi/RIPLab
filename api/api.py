import time
from flask import Flask, request
from flask_cors import CORS
from PIL import Image, ImageDraw

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

    output_img = Image.new('RGB', (int(w), int(h)))
    draw = ImageDraw.Draw(output_img)

    for x in range(output_img.width):
        for y in range(output_img.height):
            xp, yp = x + topleft[0], y + topleft[1]
            draw.point((x, y), pixels[xp, yp])
    
    output_img.save(f'crop-x{topleft[0]}-y{topleft[1]}-w{w}-h{h}.png')
    return {'x': topleft[0], 'y': topleft[1], 'w': w, 'h': h, 'your-image': 'CROPPED'}

cors = CORS(app, resources={'/*':{'origins': 'http://localhost:3000'}}) 

if __name__ == "__main__":
    app.run()
