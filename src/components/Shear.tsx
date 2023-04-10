import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  url: string;
}

function Shear(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
        <div className='operation-item flex-reverse'>
            <label className='label-right' htmlFor="deg"><h4>degrees</h4></label>
            <input type="number" id="deg" name="deg" placeholder='deg'/>
        </div>

        <div className='operation-item dir-column'>
            <h3 style={{marginTop: '0px', marginBottom: '4px'}}>Direction</h3>
            <div>
                <input type="radio" id="vertical" name="direction" value="vertical"/>
                <label htmlFor="vertical" className='label-checkbox'>Vertical</label>
            </div>
            <div>
                <input type="radio" id="horizontal" name="direction" value="horizontal"/>
                <label htmlFor="horizontal" className='label-checkbox'>Horizontal</label>
            </div>
        </div>

        <div className='operation-action'>
            <h3>Shear</h3>
        </div>

    </div>
  );
}

export default Shear;
