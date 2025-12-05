import React from 'react';
import { OverviewCards } from '../components/metrics/OverviewCards';
import { RatingTrendChart } from '../components/charts/RatingTrendChart';
import { SentimentPieChart } from '../components/charts/SentimentPieChart';
import { AppRankingTable } from '../components/metrics/AppRankingTable';
import Card from '../components/ui/Card';

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <OverviewCards />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Rating Trend">
          <RatingTrendChart />
        </Card>
        <Card title="Sentiment Distribution">
          <SentimentPieChart />
        </Card>
      </div>

      <AppRankingTable />
    </div>
  );
};

export default Dashboard;
