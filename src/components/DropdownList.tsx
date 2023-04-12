import React, { useState } from "react";
import '../css/DropdownList.css';
import { AiOutlineDownload, AiOutlineUpload } from "react-icons/ai";
import { MdOutlineRestorePage } from "react-icons/md";
import { BiUndo, BiRedo } from "react-icons/bi";
import { DropdownProp } from "../common/types";


function DropdownList (props: DropdownProp) {
  const [file, setFile] = useState<File | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
      const formData = new FormData();
      formData.append('file', event.target.files[0]);

      fetch('http://localhost:4720/upload', {
        method: 'POST',
        body: formData,
        headers: {
          'Access-Control-Allow-Origin': 'http://localhost:3000' 
        }
      })
      .then((response) => response.json())
      .then((data) => {
        props.setImageURL(data.url);
        props.setOriginal(data.url);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
  };

  const downloadImage = () => {
    fetch(props.url, {
      mode : 'no-cors',
    })
      .then(response => response.blob())
      .then(blob => {
      let blobUrl = window.URL.createObjectURL(blob);
      let a = document.createElement('a');
      a.download = props.url.replace(/^.*[\\\/]/, '');
      a.href = blobUrl;
      document.body.appendChild(a);
      a.click();
      a.remove();
    })
  }

  const resetImage = () => {
    props.setImageURL(props.original);
  }

  const undoAction = () => {
    // TODO
  }

  const redoAction = () => {
    // TODO
  }

  return (
    <div className="dropdown-header">
      <h2 className="header-title">RIPLab</h2>
      <h4 className="header-subtitle"><b>R</b>afael's <b>I</b>mage <b>P</b>rocessing <b>Lab</b></h4>

      <div className="header-buttons">
        <div className="btn" title="Upload Image">
          <input type="file" id="img-upload" accept="image*/" onChange={handleFileUpload} hidden/>
          <label htmlFor="img-upload" ><AiOutlineUpload size={42}/></label>
        </div>
        <div className="btn" title="Download Image" onClick={downloadImage}>
          <AiOutlineDownload size={42}/>
        </div>
        <div className="btn" title="Reset Image" onClick={resetImage}>
          <MdOutlineRestorePage size={42}/>
        </div>
        <div className="btn" title="Undo" onClick={undoAction}>
          <BiUndo size={42}/>
        </div>
        <div className="btn" title="Redo" onClick={redoAction}>
          <BiRedo size={42}/>
        </div>
      </div>
    </div>
  );
};

export default DropdownList;
