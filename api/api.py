# api.py
from fractions import Fraction
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from uuid import uuid4
from PIL.Image import Image
from api.crop import crop
from api.filter import generate_noise, filter
from api.flip import horizontal_flip, vertical_flip
from api.histogram import histogram, histogram_equalization
from api.kernel import kernel
from api.map import map
from api.rotate import rotate
from api.scale import scale

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'

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


@app.route('/horizontal-flip', methods=['GET', 'POST'])
@app.route('/vertical-flip', methods=['GET', 'POST'])
@app.route('/rotate', methods=['GET', 'POST'])
@app.route('/crop', methods=['GET', 'POST'])
@app.route('/scale', methods=['GET', 'POST'])
@app.route('/rotate', methods=['GET', 'POST'])
@app.route('/map', methods=['GET', 'POST'])
@app.route('/histogram', methods=['GET', 'POST'])
@app.route('/histogram-equalization', methods=['GET', 'POST'])
@app.route('/generate-noise', methods=['GET', 'POST'])
@app.route('/filter', methods=['GET', 'POST'])
@app.route('/kernel', methods=['GET', 'POST'])
def dispatch():
    operation = request.path
    method = request.method.replace('/', '')

    # Get parameters
    if request.method == 'GET':
        params = request.args
    else:
        params = request.form

    # Validate parameters for given operation
    success, validated_params, msg = validate_params(operation, params)

    if not success:
        return {'operation': operation, 'method': method, 'err': msg}

    # Load image
    img = Image.open(validated_params['url'])

    # Call operation
    if operation == 'histogram':
        histogram_dict = histogram(img)
        return {'operation': operation, 'parameters': validated_params, 'method': method, 'histogram': histogram_dict}
    else:
        new_img = call_operation(operation, img, validated_params)

    # Save image and return new image URL
    new_url = save_image(new_img, validated_params['ext'])

    return {'operation': operation, 'parameters': validated_params, 'method': method, 'url': new_url}


def validate_params(operation, params) -> tuple(bool, dict, str):
    """
    Validates the parameters for a given operation by creating a new, validated 
    dictionary of values.
    :param operation: The operation to validate parameters for
    :param params: The parameters to validate
    :return: Returns a tuple of (success, validated_params, msg)
    """
    validated_params = {}

    # Ensure that there is an image URL
    if 'url' not in params:
        return False, {}, 'No image URL'
    validated_params['url'] = params['url']
    validated_params['ext'] = validated_params['url'].split('.')[-1]
    
    # Crop validation: check that all parameters are present and valid
    if operation == 'crop':
        # Ensure that all parameters are present
        if not all(['x', 'y', 'w', 'h']) in params:
            return False, {}, 'Missing parameters'
        
        # Get parameters
        validated_params['x'] = params.get('x', 0, int)
        validated_params['y'] = params.get('y', 0, int)
        validated_params['w'] = params.get('w', 1, int)
        validated_params['h'] = params.get('h', 1, int)

        # Check that the crop is within the image bounds
        img_size = Image.open(validated_params['url']).size
        if validated_params['x'] < 0 or validated_params['y'] < 0 or validated_params['w'] < 1 or validated_params['h'] < 1:
            return False, {}, 'Invalid crop parameters, must be positive'
        if validated_params['x'] + validated_params['w'] > img_size[0] or validated_params['y'] + validated_params['h'] > img_size[1]:
            return False, {}, 'Invalid crop parameters, must be within image bounds'

    # Scaling validation
    elif operation == 'scale':
        # Ensure that a scaling type is specified and is valid
        scale_type = params.get('type')
        if scale_type is None:
            return False, {}, 'Missing scaling type'
        if not scale_type in ['nn', 'bl', 'bc']:
            return False, {}, 'Invalid scaling type'
        
        # Set other parameters based on scaling type
        validated_params['type'] = scale_type
        validated_params['w'] = params.get('w', 1, int)
        validated_params['h'] = params.get('h', 1, int)
    
    # Rotation validation
    elif operation == 'rotate':
        validated_params['deg'] = params.get('deg', 0, int)
    
    # Map validation
    elif operation == 'map':
        # Ensure that a map type is specified and is valid
        map_type = params.get('type')
        if map_type is None:
            return False, {}, 'Missing map type'
        if map_type not in ['linear', 'power']:
            return False, {}, 'Invalid map type'
        
        validated_params['type'] = params.get('type')
        
        # Set other parameters based on map type
        if validated_params['type'] == 'linear':
            validated_params['alpha'] = params.get('alpha', 1, int)
            validated_params['beta'] = params.get('beta', 0, int)
        elif validated_params['type'] == 'power':
            validated_params['gamma'] = params.get('gamma', 1, int)
    
    # Histogram validation
    elif operation == 'histogram-equalization':
        validated_params['apply_to_alpha'] = params.get('apply-to-alpha', False, bool)
    
    # Noise generation validation
    elif operation == 'generate-noise':
        validated_params['apply_to_alpha'] = params.get('apply-to-alpha', False, bool)
        validated_params['salt_chance'] = params.get('salt-chance', 5, float)
        validated_params['pepper_chance'] = params.get('pepper-chance', 5, float)
    
    # Filter validation
    elif operation == 'filter':
        # Ensure that a filter type has been given and is valid
        filter_type = params.get('type')
        if filter_type is None:
            return False, {}, 'Missing filter type'
        if not filter_type in ['min', 'max', 'median']:
            return False, {}, 'Invalid filter type'
        
        # Get other parameters
        validated_params['type'] = filter_type
        validated_params['size'] = params.get('size', 3, int)
        validated_params['apply_to_alpha'] = params.get('apply-to-alpha', False, bool)
    
    # Kernel validation
    elif operation == 'kernel':
        validated_params['apply_to_alpha'] = params.get('apply-to-alpha', False, bool)
        kernel = params.get('kernel')

        # Check if kernel is a valid matrix
        if kernel is None:
            return False, {}, 'Kernel not specified'
        first_len = len(kernel[0])
        if not all(len(x) == first_len for x in kernel[1:]):
            return False, {}, 'Kernel is not a rectangular matrix'
        
        # Convert kernel values to floats
        kernel = [[float(Fraction(i)) for i in j] for j in kernel]
        validated_params['kernel'] = kernel

    return True, validated_params, ''


def call_operation(operation, img, params) -> Image:
    """
    Calls the given operation with the given parameters on the given image.
    """
    if operation == 'crop':
        return crop(img, params)
    elif operation == 'generate-noise':
        return generate_noise(img, params)
    elif operation == 'filter':
        return filter(img, params)
    elif operation == 'horizontal-flip':
        return horizontal_flip(img)
    elif operation == 'vertical-flip':
        return vertical_flip(img)
    elif operation == 'histogram-equalization':
        return histogram_equalization(img, params)
    elif operation == 'kernel':
        return kernel(img, params)
    elif operation == 'map':
        return map(img, params)
    elif operation == 'rotate':
        return rotate(img, params)
    elif operation == 'scale':
        return scale(img, params)


def save_image(img, ext) -> str:
    """
    Saves the given image to the upload folder and returns the filename.
    """

    # Create a unique filename
    filename = str(uuid4()) + ext
    path = UPLOAD_FOLDER + filename

    # Save the image
    img.save(path)

    # Return the filename
    return filename
