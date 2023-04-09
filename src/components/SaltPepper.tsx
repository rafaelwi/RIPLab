import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  imageURL: string;
}

function SaltPepper(props: ImageOperationsProps) {
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

        <div className='operation-action'>
            <h3>Generate Noise</h3>
        </div>
    </div>
  );
}

export default SaltPepper;
