import React, { useState } from 'react';
import {GoChevronDown, GoChevronUp} from 'react-icons/go';
import '../css/Dropdown.css';


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
      <div className="dropdown-item" onClick={handleToggle}>
        <div className='dropdown-text'>
          <div className='icon'>{props.icon}</div>
          <h3>{props.title}</h3>

          <div className='chevron'>
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
