import React from 'react';
import '../css/ImageOperations.css';
import {TbFlipHorizontal, TbFlipVertical} from 'react-icons/tb';

interface ImageOperationsProps {
  imageURL: string;
}

function Flip(props: ImageOperationsProps) {
  return (
    <div className="img-operation">
      <div className="operation-btn">
        <div className="operation-icon"><TbFlipHorizontal size={20}/></div>
        <h3>Horizontal</h3>
      </div>
      <div className="operation-btn">
        <div className="operation-icon"><TbFlipVertical size={20}/></div>
        <h3>Vertical</h3>
      </div>
    </div>
  );
}

export default Flip;
