import React from 'react';
import '../css/ImageView.css';

interface ImageEditorProps {
  imageURL: string;
}

function ImageView(props: ImageEditorProps) {
  return (
    <div className="image-view">
      <img src={props.imageURL} alt="uploaded" />
    </div>
  );
}

export default ImageView;
