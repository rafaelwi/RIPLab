import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  url: string;
}

function Convolution(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
        <div className='operation-item kernel'>
            <h4>Kernel</h4>
            <textarea name="kernel" id="kernel" cols={30} rows={10} placeholder='0 -1 0&#10;-1 5 -1&#10;0 -1 0'></textarea>
        </div>

        <div className='operation-item kernel'>
          <input type="checkbox" id="apply-to-alpha" name="apply-to-alpha"/>
          <label htmlFor="apply-to-alpha" className='label-checkbox'>Apply to Alpha Channel?</label>
        </div>

        <div className='operation-action'>
            <h3>Map</h3>
        </div>
    </div>
  );
}

export default Convolution;
