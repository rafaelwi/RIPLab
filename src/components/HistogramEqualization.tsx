import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  url: string;
}

function HistogramEqualization(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
      <div className='operation-item kernel'>
        <input type="checkbox" id="apply-to-alpha" name="apply-to-alpha"/>
        <label htmlFor="apply-to-alpha" className='label-checkbox'>Apply to Alpha Channel?</label>
      </div>

      <div className='operation-action'>
          <h3>Equalize</h3>
      </div>
    </div>
  );
}

export default HistogramEqualization;
