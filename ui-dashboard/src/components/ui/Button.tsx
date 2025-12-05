import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'neutral';
}

const Button: React.FC<ButtonProps> = ({ children, className = '', variant = 'primary', ...rest }) => {
  const cls = `skeu-button ${variant === 'primary' ? 'gold-accent' : ''} ${className}`;
  return (
    <button className={cls} {...rest}>
      {children}
    </button>
  );
};

export default Button;
