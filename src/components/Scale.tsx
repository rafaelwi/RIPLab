import '../css/ImageOperations.css';
import { ImageOperationProp } from '../common/types';
import { sendCommonRequest } from '../common/utils';


function Scale(props: ImageOperationProp) {
  const scaleImage = async () => {
    // Get parameters
    const height = parseInt((document.getElementById('height') as HTMLInputElement).value);
    const width = parseInt((document.getElementById('width') as HTMLInputElement).value);
    const type = (document.getElementById('nn') as HTMLInputElement)?.checked ? 'nn' : 'bl';

    // Make request
    sendCommonRequest(
      'http://localhost:4720/scale',
      JSON.stringify({ url: props.url, h: height, w: width, type }),
      props.setImageURL
    )
  }

  const imageFileWidth = (document.getElementById("image-view-image") as HTMLImageElement)?.naturalWidth;
  const imageFileHeight = (document.getElementById("image-view-image") as HTMLImageElement)?.naturalHeight;

  return (
    <div className="img-operation">
      <div className='operation-item'>
        <label className='label-left' htmlFor="height"><h4>Height</h4></label>
        <input type="number" id="height" name="height"
          min="1" placeholder='height' value={imageFileWidth} />
      </div>
      <div className='operation-item'>
        <label className='label-left' htmlFor="width"><h4>Width</h4></label>
        <input type="number" id="width" name="width"
          min="1" placeholder='width' value={imageFileHeight}/>
      </div>

      <div className='operation-item dir-column'>
        <h3 style={{ marginTop: '0px', marginBottom: '4px' }}>Method</h3>
        <div>
          <input type="radio" id="nn" name="method" value="nn" />
          <label htmlFor="nn" className='label-checkbox'>Nearest Neighbour</label>
        </div>
        <div>
          <input type="radio" id="bl" name="method" value="bl" />
          <label htmlFor="bl" className='label-checkbox'>Bilinear</label>
        </div>
      </div>

      <div className='operation-action' onClick={scaleImage}>
        <h3>Scale</h3>
      </div>

    </div>
  );
}

export default Scale;
