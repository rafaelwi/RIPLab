import React, { useState } from "react";
import '../css/DropdownList.css';
import {GoChevronDown, GoChevronUp} from 'react-icons/go';

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
    <div className="dropdown-item"
      onClick={handleToggle}
      style={{ 
        marginBottom: '16px',
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

      {isOpen && (
        <div className="dropdown-content"
          style={{
            backgroundColor: "#fff",
            padding: "8px",
            border: "1px solid #ccc",
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
    <div style={{margin: '16px'}}>
      {items.map((item, index) => (
        <Dropdown key={index} {...item} />
      ))}
    </div>
  );
};

export default DropdownList;
