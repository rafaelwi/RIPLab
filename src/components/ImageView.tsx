import React from 'react';
import '../css/ImageView.css';

interface ImageEditorProps {
  url: string;
}

function ImageView(props: ImageEditorProps) {
  return (
    <div className="image-view">
      <img src={props.url} alt="uploaded" />
    </div>
  );
}

export default ImageView;
