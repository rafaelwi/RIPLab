import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  url: string;
}

function PowerLaw(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
        <div className='operation-item'>
            <label className='label-left' htmlFor="gamma"><h4>gamma</h4></label>
            <input type="number" id="gamma" name="gamma" placeholder='𝜸'/>
        </div>

        <div className='operation-action'>
            <h3>Map</h3>
        </div>
    </div>
  );
}

export default PowerLaw;
