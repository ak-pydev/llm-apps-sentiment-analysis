import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useAppSentimentDist } from '../../hooks/useAppSentimentDist';

const DEMO_APP = 'gemini';
const COLORS = ['#22c55e', '#f59e42', '#64748b'];

export const SentimentPieChart: React.FC = () => {
  const { data, loading, error } = useAppSentimentDist(DEMO_APP);

  if (loading) return <div className="h-80 bg-gray-100 animate-pulse rounded-lg" />;
  if (error) return <div className="text-red-500">{error}</div>;
  if (!data) return <div className="h-80 flex items-center justify-center text-gray-400">No data</div>;

  const chartData = [
    { name: 'Positive', value: data.positive },
    { name: 'Negative', value: data.negative },
    { name: 'Neutral', value: data.neutral },
  ];

  return (
    <ResponsiveContainer width="100%" height={320}>
      <PieChart>
        <Pie
          data={chartData}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={100}
          label
        >
          {chartData.map((entry, idx) => (
            <Cell key={entry.name} fill={COLORS[idx]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};
