import '../css/ImageOperations.css';
import { ImageOperationProp } from '../common/types';
import { sendCommonRequest } from '../common/utils';


function SaltPepper(props: ImageOperationProp) {
  const generateNoise = async () => {
    // Get parameters
    const salt = parseFloat((document.getElementById('salt') as HTMLInputElement)?.value);
    const pepper = parseFloat((document.getElementById('pepper') as HTMLInputElement)?.value);
    const applyToAlpha = (document.getElementById('noise-apply-to-alpha') as HTMLInputElement).checked;

    // Make request
    sendCommonRequest(
      'http://localhost:4720/generate-noise',
      JSON.stringify({ 
        url: props.url, 'salt-chance': salt ? salt : 0, 
        'pepper-chance': pepper ? pepper : 0, 'apply-to-alpha': applyToAlpha
      }),
      props.setImageURL
    )
  }

  return (
    <div className="img-operation">
        <div className='operation-item'>
            <label className='label-left' htmlFor="salt"><h4>Salt</h4></label>
            <input type="number" id="salt" name="salt" placeholder='salt'/>
        </div>

        <div className='operation-item'>
            <label className='label-left' htmlFor="pepper"><h4>Pepper</h4></label>
            <input type="number" id="pepper" name="pepper" placeholder='pepper'/>
        </div>

        <div className='operation-item kernel'>
          <input type="checkbox" id="noise-apply-to-alpha" name="noise-apply-to-alpha"/>
          <label htmlFor="noise-apply-to-alpha" className='label-checkbox'>Apply to Alpha Channel?</label>
        </div>

        <div className='operation-action' onClick={generateNoise}>
            <h3>Generate Noise</h3>
        </div>
    </div>
  );
}

export default SaltPepper;
