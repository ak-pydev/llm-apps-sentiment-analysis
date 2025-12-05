import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

interface AppLayoutProps {
  children: React.ReactNode;
  title?: string;
  onNavigate?: (page: string) => void;
}

export const AppLayout: React.FC<AppLayoutProps> = ({
  children,
  title = 'Dashboard',
  onNavigate,
}) => {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar onNavigate={onNavigate} />
      <div className="flex-1 flex flex-col">
        <Header title={title} />
        <main className="flex-1 overflow-auto p-6">{children}</main>
      </div>
    </div>
  );
};

export default AppLayout;
