import { useEffect, useState } from 'react';
import { client } from '../api/client';

export interface DashboardOverview {
  total_reviews: number;
  total_apps: number;
  avg_rating: number | null;
  positive_percentage: number | null;
  updated_at: string;
}

export const useDashboardOverview = () => {
  const [data, setData] = useState<DashboardOverview | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    client.get<DashboardOverview>('/dashboard/overview')
      .then(setData)
      .catch((err) => {
        setError('Failed to fetch dashboard overview');
        console.error(err);
      })
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
};
