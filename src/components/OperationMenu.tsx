import React from 'react';

interface MenuButtonProps {
  label: string;
  onClick?: () => void;
}

const SidebarButton: React.FC<MenuButtonProps> = ({ label, onClick }) => {
  return (
    <button onClick={onClick} style={{width:'100%', marginBottom: 16 }}>
      {label}
    </button>
  );
};

interface OperationMenuProps {
  buttons: Array<{
    label: string;
    onClick?: () => void;
    wide?: boolean;
  }>;
}

const OperationMenu: React.FC<OperationMenuProps> = ({ buttons }) => {
  return (
    <div
      style={{
        // width: '15%',
        padding: '16px',
        backgroundColor: '#f5f5f5',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',

      }}
    >
      {buttons.map((button, i) => {
          return (
            <SidebarButton
              key={i}
              label={button.label}
              onClick={button.onClick}
            />
          );
      })}
    </div>
  );
};

export default OperationMenu;
