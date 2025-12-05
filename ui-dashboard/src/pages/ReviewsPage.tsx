import React from 'react';
import { TopReviewsTable } from '../components/metrics/TopReviewsTable';

const ReviewsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <TopReviewsTable />
    </div>
  );
};

export default ReviewsPage;
