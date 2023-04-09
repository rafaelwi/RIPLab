import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  imageURL: string;
}

function Crop(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
        <div className='operation-item'>
            <label className='label-left' htmlFor="x"><h4>x</h4></label>
            <input type="number" id="x" name="x"
                min="0" placeholder='x'/>
        </div>
        <div className='operation-item'>
            <label className='label-left' htmlFor="y"><h4>y</h4></label>
            <input type="number" id="y" name="y"
                min="0" placeholder='y'/>
        </div>

        <div className='operation-item'>
            <label className='label-left' htmlFor="height"><h4>Height</h4></label>
            <input type="number" id="height" name="height"
                min="1" placeholder='height'/>
        </div>
        <div className='operation-item'>
            <label className='label-left' htmlFor="height"><h4>Width</h4></label>
            <input type="number" id="width" name="width"
                min="1" placeholder='width'/>
        </div>

        <div className='operation-action'>
            <h3>Crop</h3>
        </div>

    </div>
  );
}

export default Crop;
