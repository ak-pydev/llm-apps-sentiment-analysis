import React from 'react';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  className?: string;
  variant?: 'default' | 'skeuomorphic';
}

const Card: React.FC<CardProps> = ({ children, title, className = '', variant = 'skeuomorphic' }) => {
  const base = variant === 'skeuomorphic' ? 'skeu-card' : 'bg-white rounded-lg shadow';
  return (
    <div className={`${base} ${className}`}>
      {title && <div className="card-header"><h3 className="text-lg font-semibold mb-0 emboss">{title}</h3></div>}
      <div className="card-body">{children}</div>
    </div>
  );
};

export default Card;
