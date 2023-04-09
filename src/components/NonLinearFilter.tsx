import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  imageURL: string;
}

function NonLinearFilter(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
      <div className='operation-item'>
        <label className='label-left' htmlFor="size"><h4>Size</h4></label>
        <input type="number" id="size" name="size"
          min="1" placeholder='size' />
      </div>

      <div className='operation-item dir-column'>
        <h3 style={{ marginTop: '0px', marginBottom: '4px' }}>Method</h3>
        <div>
          <input type="radio" id="min" name="type" value="min" />
          <label htmlFor="min" className='label-checkbox'>Min</label>
        </div>
        <div>
          <input type="radio" id="median" name="type" value="median" />
          <label htmlFor="median" className='label-checkbox'>Median</label>
        </div>
        <div>
          <input type="radio" id="max" name="type" value="max" />
          <label htmlFor="max" className='label-checkbox'>Max</label>
        </div>
      </div>

      <div className='operation-item kernel'>
        <input type="checkbox" id="apply-to-alpha" name="apply-to-alpha"/>
        <label htmlFor="apply-to-alpha" className='label-checkbox'>Apply to Alpha Channel?</label>
      </div>

      <div className='operation-action'>
        <h3>Filter</h3>
      </div>

    </div>
  );
}

export default NonLinearFilter;
