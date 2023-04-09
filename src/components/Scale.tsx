import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  imageURL: string;
}

function Scale(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
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

        <div className='operation-item dir-column'>
            <h3 style={{marginTop: '0px', marginBottom: '4px'}}>Method</h3>
            <div>
                <input type="radio" id="nn" name="method" value="30"/>
                <label htmlFor="nn">Nearest Neighbour</label>
            </div>
            <div>
                <input type="radio" id="bl" name="method" value="60"/>
                <label htmlFor="bl">Bilinear</label>
            </div>
        </div>

        <div className='operation-action'>
            <h3>Scale</h3>
        </div>

    </div>
  );
}

export default Scale;