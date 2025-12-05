import React from 'react';
import Card from '../ui/Card';
import { useDashboardOverview } from '../../hooks/useDashboardOverview';

export const OverviewCards: React.FC = () => {
  const { data, loading, error } = useDashboardOverview();

  const stats = [
    { label: 'Total Reviews', value: data?.total_reviews ?? '—', color: 'bg-blue-100' },
    { label: 'Avg Rating', value: data?.avg_rating?.toFixed(2) ?? '—', color: 'bg-green-100' },
    { label: 'Positive %', value: data?.positive_percentage != null ? `${data.positive_percentage.toFixed(1)}%` : '—', color: 'bg-emerald-100' },
    { label: 'Apps', value: data?.total_apps ?? '—', color: 'bg-purple-100' },
  ];

  if (loading) return <div className="h-24 animate-pulse bg-gray-100 rounded" />;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat) => (
        <Card key={stat.label} className={stat.color}>
          <p className="text-gray-600 text-sm">{stat.label}</p>
          <p className="text-3xl font-bold mt-2">{stat.value}</p>
        </Card>
      ))}
    </div>
  );
};
