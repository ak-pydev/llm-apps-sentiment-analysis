import { useEffect, useState } from 'react';
import { client } from '../api/client';

interface DashboardMetrics {
  totalReviews: number;
  avgRating: number;
  sentimentDistribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
  topApps: Array<{
    appName: string;
    reviews: number;
    rating: number;
  }>;
}

export const useDashboardMetrics = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        setLoading(true);
        const data = await client.get<DashboardMetrics>('/dashboard/metrics');
        setMetrics(data);
      } catch (err) {
        setError('Failed to fetch dashboard metrics');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  return { metrics, loading, error };
};
