import React, { useState } from "react";
import '../css/DropdownList.css';
import {GoChevronDown, GoChevronUp} from 'react-icons/go';
import { AiOutlineDownload, AiOutlineUpload } from "react-icons/ai";
import { MdOutlineRestorePage } from "react-icons/md";
import { BiUndo, BiRedo } from "react-icons/bi";
import { ImageOperationProp } from "../common/types";


interface DropdownProps {
  title: string;
  content: React.ReactNode;
  icon?: React.ReactNode;
}


function DropdownList (props: ImageOperationProp) {
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
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
  };

  return (
    <div className="dropdown-header">
      <h2 className="header-title">RIPLab</h2>
      <h4 className="header-subtitle"><b>R</b>afael's <b>I</b>mage <b>P</b>rocessing <b>Lab</b></h4>

      <div className="header-buttons">
        <div className="btn" title="Upload Image">
          <input type="file" id="img-upload" accept="image*/" onChange={handleFileUpload} hidden/>
          <label htmlFor="img-upload" ><AiOutlineUpload size={42}/></label>
        </div>
        <div className="btn" title="Download Image">
          <AiOutlineDownload size={42}/>
        </div>
        <div className="btn" title="Reset Image">
          <MdOutlineRestorePage size={42}/>
        </div>
        <div className="btn" title="Undo">
          <BiUndo size={42}/>
        </div>
        <div className="btn" title="Redo">
          <BiRedo size={42}/>
        </div>
      </div>
    </div>
  );
};

export default DropdownList;
