import '../css/ImageOperations.css';
import { ImageOperationProp } from '../common/types';
import { sendCommonRequest } from '../common/utils';


function HistogramEqualization(props: ImageOperationProp) {
  const equalize = async () => {
    // Get parameters
    const applyToAlpha = (document.getElementById('apply-to-alpha') as HTMLInputElement).checked;

    // Make request
    sendCommonRequest(
      'http://localhost:4720/histogram-equalization',
      JSON.stringify({ url: props.url, 'apply-to-alpha': applyToAlpha }),
      props.setImageURL
    );
  }


  return (
    <div className="img-operation">
      <div className='operation-item kernel'>
        <input type="checkbox" id="apply-to-alpha" name="apply-to-alpha"/>
        <label htmlFor="apply-to-alpha" className='label-checkbox'>Apply to Alpha Channel?</label>
      </div>

      <div className='operation-action' onClick={equalize}>
          <h3>Equalize</h3>
      </div>
    </div>
  );
}

export default HistogramEqualization;
