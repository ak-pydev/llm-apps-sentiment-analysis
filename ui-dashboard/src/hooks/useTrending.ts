import { useEffect, useState } from 'react';
import { client } from '../api/client';

interface TrendingItem {
  keyword: string;
  count: number;
  sentiment: string;
}

export const useTrending = () => {
  const [trending, setTrending] = useState<TrendingItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTrending = async () => {
      try {
        setLoading(true);
        const data = await client.get<TrendingItem[]>('/dashboard/trending');
        setTrending(data);
      } catch (err) {
        setError('Failed to fetch trending data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTrending();
  }, []);

  return { trending, loading, error };
};
