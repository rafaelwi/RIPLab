import '../css/ImageOperations.css';
import { ImageOperationProp } from '../common/types';
import { sendCommonRequest } from '../common/utils';


function PowerLaw(props: ImageOperationProp) {
  const mapImage = async () => {
    // Get parameters
    const gamma = parseFloat((document.getElementById('gamma') as HTMLInputElement).value);
    console.log(gamma)

    // Make request
    sendCommonRequest(
      'http://localhost:4720/map',
      JSON.stringify({ url: props.url, type: 'power', gamma }),
      props.setImageURL
    )
  }

  return (
    <div className="img-operation">
        <div className='operation-item'>
            <label className='label-left' htmlFor="gamma"><h4>gamma</h4></label>
            <input type="number" id="gamma" name="gamma" placeholder='𝜸'/>
        </div>

        <div className='operation-action' onClick={mapImage}>
            <h3>Map</h3>
        </div>
    </div>
  );
}

export default PowerLaw;
