import React from 'react';
import Card from '../ui/Card';

export const TopReviewsTable: React.FC = () => {
  return (
    <Card title="Top Reviews">
      <div className="space-y-4">
        <p className="text-gray-500 text-center py-4">No reviews available</p>
      </div>
    </Card>
  );
};
