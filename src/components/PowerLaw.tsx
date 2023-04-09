import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  imageURL: string;
}

function PowerLaw(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
        <div className='operation-item'>
            <label className='label-left' htmlFor="alpha"><h4>gamma</h4></label>
            <input type="number" id="alpha" name="alpha" placeholder='𝜸'/>
        </div>

        <div className='operation-action'>
            <h3>Map</h3>
        </div>
    </div>
  );
}

export default PowerLaw;
