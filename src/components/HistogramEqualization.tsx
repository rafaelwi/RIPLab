import React from 'react';
import '../css/ImageOperations.css';
import { ImageOperationProp } from '../common/types';


function HistogramEqualization(props: ImageOperationProp) {
  const equalize = async () => {
    // Get parameters
    const applyToAlpha = document.getElementById('apply-to-alpha') as HTMLInputElement;

    // Make request
    const resp = await fetch('http://localhost:4720/histogram-equalization', {
      method: 'POST',
      body: JSON.stringify({
        url: props.url,
        'apply-to-alpha': applyToAlpha.checked
      }),
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'http://localhost:3000'
      }
    })
    .then((response) => response.json())
    .then((response) => {
      const newURL : string = response.url;
      props.setImageURL(newURL);
    });
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
