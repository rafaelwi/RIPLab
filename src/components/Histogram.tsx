import React, { useState } from 'react';
import '../css/ImageOperations.css';
import { AgChartsReact } from 'ag-charts-react';
import { AgChart, AgChartOptions } from 'ag-charts-community';

interface ImageOperationsProps {
  url: string;
}

function Histogram(props: ImageOperationsProps) {
  // const url = props.url.replace('http://localhost:4720/', '');
  const [options, setOptions] = useState<AgChartOptions>({
    autoSize: true,
    title: { text: 'Image Histogram' },
    legend: {
      position: 'bottom',
    }
  });

  const calculateHistogram = async () => {
    const resp = await fetch('http://localhost:4720/histogram', { 
      method: 'POST',
      body: JSON.stringify({url: props.url}),
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'http://localhost:3000' 
      }
    })
    .then((response) => response.json())
    .then((response) => {
      setOptions({
        title: {text: 'Image Histogram'}, 
        data: response.data, 
        series: response.series, 
        autoSize: true,
        legend: {
          position: 'bottom',
        }
      });
    });
  }

  return (
    <div className="img-operation">
        <div className='operation-action' onClick={calculateHistogram}>
            <h3>Calculate</h3>
        </div>
        <div className='operation-result'>
          <AgChartsReact options={options} />
        </div>
    </div>
  );
}

export default Histogram;
