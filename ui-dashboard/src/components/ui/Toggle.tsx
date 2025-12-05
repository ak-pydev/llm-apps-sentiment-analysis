import React from 'react';

interface ToggleProps {
  checked?: boolean;
  onChange?: (next: boolean) => void;
}

const Toggle: React.FC<ToggleProps> = ({ checked = false, onChange }) => {
  return (
    <div
      role="switch"
      aria-checked={checked}
      tabIndex={0}
      onClick={() => onChange && onChange(!checked)}
      className={`skeu-toggle ${checked ? 'on' : ''}`}
    >
      <div className="knob" />
    </div>
  );
};

export default Toggle;
