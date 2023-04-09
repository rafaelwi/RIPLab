import React, { useState } from 'react';
import {GoChevronDown, GoChevronUp} from 'react-icons/go';


interface ImageEditorProps {
  title: string
  content: React.ReactNode;
  icon?: React.ReactNode;
}

function Dropdown(props: ImageEditorProps) {
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
          <div style={{display: 'block', margin: 'auto 10px auto 0'}}>{props.icon}</div>
          <h3 style={{}}>{props.title}</h3>

          <div style={{marginLeft: 'auto'}}>
            {isOpen ? <GoChevronUp /> : <GoChevronDown />}
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="dropdown-content">
          {props.content}
        </div>
      )}
    </div>
  );
}

export default Dropdown;
