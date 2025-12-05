import React from 'react';
import { Link } from 'react-router-dom';

interface SidebarProps {
  onNavigate?: (page: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onNavigate }) => {
  const items = [
    { label: 'Dashboard', path: '/' },
    { label: 'Apps', path: '/apps' },
    { label: 'Reviews', path: '/reviews' },
  ];

  return (
    <aside className="w-64 bg-gray-900 text-white h-screen p-4">
      <nav className="space-y-2">
        {items.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            onClick={() => onNavigate?.(item.path)}
            className="w-full text-left px-4 py-2 rounded hover:bg-gray-800 transition block"
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
};
