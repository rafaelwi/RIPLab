import '../css/ImageOperations.css';
import { ImageOperationProp } from '../common/types';
import { sendCommonRequest } from '../common/utils';

function Crop(props: ImageOperationProp) {
  const cropImage = async () => {
    // Get parameters
    const x = parseInt((document.getElementById('x') as HTMLInputElement).value);
    const y = parseInt((document.getElementById('y') as HTMLInputElement).value);
    const height = parseInt((document.getElementById('crop-h') as HTMLInputElement).value);
    const width = parseInt((document.getElementById('crop-w') as HTMLInputElement).value);

    // Make request
    sendCommonRequest(
      'http://localhost:4720/crop',
      JSON.stringify({ url: props.url, x, y, h: height, w: width }),
      props.setImageURL
    )
  }

  return (
    <div className="img-operation">
        <div className='operation-item'>
            <label className='label-left' htmlFor="x"><h4>x</h4></label>
            <input type="number" id="x" name="x"
                min="0" placeholder='x'/>
        </div>
        <div className='operation-item'>
            <label className='label-left' htmlFor="y"><h4>y</h4></label>
            <input type="number" id="y" name="y"
                min="0" placeholder='y'/>
        </div>

        <div className='operation-item'>
            <label className='label-left' htmlFor="crop-h"><h4>Height</h4></label>
            <input type="number" id="crop-h" name="crop-h"
                min="1" placeholder='height'/>
        </div>
        <div className='operation-item'>
            <label className='label-left' htmlFor="crop-w"><h4>Width</h4></label>
            <input type="number" id="crop-w" name="crop-w"
                min="1" placeholder='width'/>
        </div>

        <div className='operation-action' onClick={cropImage}>
            <h3>Crop</h3>
        </div>

    </div>
  );
}

export default Crop;
