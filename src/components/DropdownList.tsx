import React, { useState } from "react";
import '../css/DropdownList.css';
import {GoChevronDown, GoChevronUp} from 'react-icons/go';
import { AiOutlineDownload, AiOutlineUpload } from "react-icons/ai";
import { MdOutlineRestorePage } from "react-icons/md";
import { BiUndo, BiRedo } from "react-icons/bi";


interface DropdownProps {
  title: string;
  content: React.ReactNode;
  icon?: React.ReactNode;
}

const Dropdown = ({ title, content, icon }: DropdownProps) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="dropdown">
      <div className="dropdown-item"
        onClick={handleToggle}
        style={{ 
          display: 'flex',
          flexFlow: 'row wrap',
          cursor: 'pointer',
          flexDirection: 'column'
      }}>
        <div style={{display: 'flex', alignItems: 'baseline', textAlign: 'center'}}>
          <div style={{display: 'block', margin: 'auto 10px auto 0'}}>{icon}</div>
          <h3 style={{}}>{title}</h3>

          <div style={{marginLeft: 'auto'}}>
            {isOpen ? <GoChevronUp /> : <GoChevronDown />}
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="dropdown-content"
          style={{
            backgroundColor: "#fff",
            padding: "8px",
            border: "1px solid #ccc",
            marginBottom: '16px',
          }}
        >
          {content}
        </div>
      )}
    </div>
  );
};

interface DropdownListProps {
  items: DropdownProps[];
}

const DropdownList = ({ items }: DropdownListProps) => {
  return (
    <div>
      <div className="dropdown-header">
        <h2 className="header-title">RIPLab</h2>
        <h4 className="header-subtitle"><b>R</b>afael's <b>I</b>mage <b>P</b>rocessing <b>Lab</b></h4>
        <div className="header-buttons">
          <div className="btn" title="Upload Image">
            <AiOutlineUpload size={42}/>
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
      <div style={{margin: '8px'}}>
        {items.map((item, index) => (
          <Dropdown key={index} {...item} />
        ))}
      </div>
    </div>
  );
};

export default DropdownList;
