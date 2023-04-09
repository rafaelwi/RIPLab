import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  imageURL: string;
}

function LinearMap(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
        <div className='operation-item'>
            <label className='label-left' htmlFor="alpha"><h4>⍺lpha</h4></label>
            <input type="number" id="alpha" name="alpha" placeholder='⍺'/>
        </div>

        <div className='operation-item'>
            <label className='label-left' htmlFor="beta"><h4>βeta</h4></label>
            <input type="number" id="beat" name="beta" placeholder='β'/>
        </div>

        <div className='operation-action'>
            <h3>Map</h3>
        </div>
    </div>
  );
}

export default LinearMap;
