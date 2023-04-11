import '../css/ImageOperations.css';
import { ImageOperationProp } from '../common/types';
import { sendCommonRequest } from '../common/utils';


function LinearMap(props: ImageOperationProp) {
  const mapImage = async () => {
    // Get parameters
    const alpha = parseFloat((document.getElementById('alpha') as HTMLInputElement).value);
    const beta = parseFloat((document.getElementById('beta') as HTMLInputElement).value);

    // Make request
    sendCommonRequest(
      'http://localhost:4720/map',
      JSON.stringify({ url: props.url, type: 'linear', alpha, beta }),
      props.setImageURL
    )
  }

  return (
    <div className="img-operation">
        <div className='operation-item'>
            <label className='label-left' htmlFor="alpha"><h4>⍺lpha</h4></label>
            <input type="number" id="alpha" name="alpha" placeholder='⍺'/>
        </div>

        <div className='operation-item'>
            <label className='label-left' htmlFor="beta"><h4>βeta</h4></label>
            <input type="number" id="beta" name="beta" placeholder='β'/>
        </div>

        <div className='operation-action' onClick={mapImage}>
            <h3>Map</h3>
        </div>
    </div>
  );
}

export default LinearMap;
