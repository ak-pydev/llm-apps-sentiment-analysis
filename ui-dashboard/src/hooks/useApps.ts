import { useEffect, useState } from 'react';
import { client } from '../api/client';

export const useApps = () => {
  const [apps, setApps] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchApps = async () => {
      try {
        setLoading(true);
        const data = await client.get<string[]>('/apps');
        setApps(data);
      } catch (err) {
        setError('Failed to fetch apps');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchApps();
  }, []);

  return { apps, loading, error };
};
