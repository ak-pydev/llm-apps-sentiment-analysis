import { useEffect, useState } from 'react';
import { client } from '../api/client';

export interface SentimentDist {
  app_name: string;
  positive: number;
  negative: number;
  neutral: number;
}

export const useAppSentimentDist = (appName: string) => {
  const [data, setData] = useState<SentimentDist | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!appName) return;
    setLoading(true);
    client.get<SentimentDist>(`/apps/${appName}/sentiment-dist`)
      .then(setData)
      .catch((err) => {
        setError('Failed to fetch sentiment distribution');
        console.error(err);
      })
      .finally(() => setLoading(false));
  }, [appName]);

  return { data, loading, error };
};
