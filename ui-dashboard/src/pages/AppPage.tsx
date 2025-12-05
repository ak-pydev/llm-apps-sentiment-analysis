import React from 'react';
import { useApps } from '../hooks/useApps';
import { Loader } from '../components/ui/Loader';
import { Error } from '../components/ui/Error';

const AppPage: React.FC = () => {
  const { apps, loading, error } = useApps();

  if (loading) return <Loader message="Loading apps..." />;
  if (error) return <Error message={error} />;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {apps.map((app) => (
        <div key={app.id} className="bg-white rounded-lg shadow p-4">
          <h3 className="font-semibold text-lg">{app.name}</h3>
          <p className="text-gray-500 text-sm">ID: {app.id}</p>
        </div>
      ))}
      {apps.length === 0 && <p className="text-gray-500">No apps found</p>}
    </div>
  );
};

export default AppPage;
