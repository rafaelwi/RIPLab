import time
from flask import Flask
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


cors = CORS(app, resources={'/*':{'origins': 'http://localhost:3000'}}) 

if __name__ == "__main__":
    app.run()
