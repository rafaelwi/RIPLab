import React from 'react';
import '../css/ImageOperations.css';

interface ImageOperationsProps {
  url: string;
}

function Histogram(props: ImageOperationsProps) {
  const url = props.url.replace('http://localhost:4720/', '');

  const calculateHistogram = async () => {
    const resp = await fetch('http://localhost:4720/histogram', { 
      method: 'POST',
      body: JSON.stringify({ url }),
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'http://localhost:3000' 
      }
    })
    .then((response) => response.json())
    .then((data) => {
      console.log(data)
    });
  }

  return (
    <div className="img-operation">
        <div className='operation-action' onClick={calculateHistogram}>
            <h3>Calculate</h3>
        </div>
    </div>
  );
}

export default Histogram;
