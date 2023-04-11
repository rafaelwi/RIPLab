import React from 'react';
import '../css/ImageOperations.css';
import { sendCommonRequest } from '../common/utils';
import { ImageOperationProp } from '../common/types';


function Rotate(props: ImageOperationProp) {
  const rotateImage = async () => {
    // Get parameters
    const deg = parseFloat((document.getElementById('rotate-deg') as HTMLInputElement).value);
    sendCommonRequest(
      'http://localhost:4720/rotate',
      JSON.stringify({ url: props.url, deg }),
      props.setImageURL
    )
  }

  return (
    <div className="img-operation">
        <div className='operation-item flex-reverse'>
            <label className='label-right' htmlFor="rotate-deg"><h4>degrees</h4></label>
            <input type="number" id="rotate-deg" name="rotate-deg" placeholder='deg'/>
        </div>

        <div className='operation-action' onClick={rotateImage}>
            <h3>Rotate</h3>
        </div>

    </div>
  );
}

export default Rotate;
