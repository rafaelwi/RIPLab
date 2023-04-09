import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  imageURL: string;
}

function Rotate(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
        <div className='operation-item flex-reverse'>
            <label className='label-right' htmlFor="deg"><h4>Degrees</h4></label>
            <input type="number" id="deg" name="deg" placeholder='deg'/>
        </div>

        <div className='operation-action'>
            <h3>Rotate</h3>
        </div>

    </div>
  );
}

export default Rotate;
