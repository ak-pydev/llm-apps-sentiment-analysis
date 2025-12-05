import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { useAppDailyStats } from '../../hooks/useAppDailyStats';

// For demo, use first app in list. In production, make appName selectable.
const DEMO_APP = 'gemini';

export const RatingTrendChart: React.FC = () => {
  const { data, loading, error } = useAppDailyStats(DEMO_APP);

  if (loading) return <div className="h-80 bg-gray-100 animate-pulse rounded-lg" />;
  if (error) return <div className="text-red-500">{error}</div>;
  if (!data.length) return <div className="h-80 flex items-center justify-center text-gray-400">No data</div>;

  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data} margin={{ left: 8, right: 8, top: 16, bottom: 8 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis domain={[0, 5]} tick={{ fontSize: 12 }} />
        <Tooltip />
        <Line type="monotone" dataKey="avg_rating" stroke="#2563eb" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
};
