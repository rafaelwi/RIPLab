import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  imageURL: string;
}

function Histogram(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
        <div className='operation-action'>
            <h3>Calculate</h3>
        </div>
    </div>
  );
}

export default Histogram;
