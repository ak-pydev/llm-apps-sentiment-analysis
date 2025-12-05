import { useEffect, useState } from 'react';
import { client } from '../api/client';

export interface DailyStat {
  date: string;
  total_reviews: number;
  avg_rating: number;
}

export const useAppDailyStats = (appName: string, days = 30) => {
  const [data, setData] = useState<DailyStat[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!appName) return;
    setLoading(true);
    client.get<DailyStat[]>(`/apps/${appName}/daily-stats?days=${days}`)
      .then(setData)
      .catch((err) => {
        setError('Failed to fetch daily stats');
        console.error(err);
      })
      .finally(() => setLoading(false));
  }, [appName, days]);

  return { data, loading, error };
};
