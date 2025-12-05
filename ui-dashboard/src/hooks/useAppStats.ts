import { useEffect, useState } from 'react';
import { client } from '../api/client';

interface AppStats {
  appName: string;
  totalReviews: number;
  avgRating: number;
  sentiment: {
    positive: number;
    negative: number;
    neutral: number;
  };
}

export const useAppStats = (appName?: string) => {
  const [stats, setStats] = useState<AppStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!appName) return;

    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await client.get<AppStats>(`/apps/${appName}/stats`);
        setStats(data);
      } catch (err) {
        setError('Failed to fetch app stats');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [appName]);

  return { stats, loading, error };
};
