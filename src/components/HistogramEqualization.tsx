import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  imageURL: string;
}

function HistogramEqualization(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
        <div className='operation-action'>
            <h3>Equalize</h3>
        </div>
    </div>
  );
}

export default HistogramEqualization;
