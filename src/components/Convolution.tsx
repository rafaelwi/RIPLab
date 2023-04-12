import '../css/ImageOperations.css';
import { ImageOperationProp } from '../common/types';
import { sendCommonRequest } from '../common/utils';


function Convolution(props: ImageOperationProp) {
  const convolve = async () => {
    // Get parameters
    const kernel = (document.getElementById('kernel') as HTMLInputElement).value;
    const applyToAlpha = (document.getElementById('convolution-apply-to-alpha') as HTMLInputElement).checked;

    // Make request
    sendCommonRequest(
      'http://localhost:4720/kernel',
      JSON.stringify({ url: props.url, kernel, 'apply-to-alpha': applyToAlpha }),
      props.setImageURL
    )
    console.log(kernel);
  }

  return (
    <div className="img-operation">
        <div className='operation-item kernel'>
            <h4>Kernel</h4>
            <textarea name="kernel" id="kernel" cols={30} rows={10} placeholder='0 -1 0&#10;-1 5 -1&#10;0 -1 0'></textarea>
        </div>

        <div className='operation-item kernel'>
          <input type="checkbox" id="convolution-apply-to-alpha" name="convolution-apply-to-alpha"/>
          <label htmlFor="convolution-apply-to-alpha" className='label-checkbox'>Apply to Alpha Channel?</label>
        </div>

        <div className='operation-action' onClick={convolve}>
            <h3>Map</h3>
        </div>
    </div>
  );
}

export default Convolution;
