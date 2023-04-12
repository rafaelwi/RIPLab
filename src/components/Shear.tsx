import '../css/ImageOperations.css';
import { ImageOperationProp } from '../common/types';
import { sendCommonRequest } from '../common/utils';

function Shear(props: ImageOperationProp) {
  const shearImage = async () => {
    // Get parameters
    const deg = parseFloat((document.getElementById('shear-deg') as HTMLInputElement).value);
    const direction = (document.querySelector('input[name="direction"]:checked') as HTMLInputElement)?.value;
    
    sendCommonRequest(
      'http://localhost:4720/shear',
      JSON.stringify({ url: props.url, deg, direction }),
      props.setImageURL
    )
  }

  return (
    <div className="img-operation">
        <div className='operation-item flex-reverse'>
            <label className='label-right' htmlFor="shear-deg"><h4>degrees</h4></label>
            <input type="number" id="shear-deg" name="shear-deg" placeholder='deg'/>
        </div>

        <div className='operation-item dir-column'>
            <h3 className='text-header'>Direction</h3>
            <div>
                <input type="radio" id="vertical" name="direction" value="vertical"/>
                <label htmlFor="vertical" className='label-checkbox'>Vertical</label>
            </div>
            <div>
                <input type="radio" id="horizontal" name="direction" value="horizontal"/>
                <label htmlFor="horizontal" className='label-checkbox'>Horizontal</label>
            </div>
        </div>

        <div className='operation-action' onClick={shearImage}>
            <h3>Shear</h3>
        </div>

    </div>
  );
}

export default Shear;
