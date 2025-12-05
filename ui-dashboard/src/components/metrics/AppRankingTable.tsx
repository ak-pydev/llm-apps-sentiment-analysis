import React from 'react';
import Card from '../ui/Card';

export const AppRankingTable: React.FC = () => {
  return (
    <Card title="Top Apps">
      <table className="w-full">
        <thead>
          <tr className="border-b">
            <th className="text-left py-2">App Name</th>
            <th className="text-left py-2">Reviews</th>
            <th className="text-left py-2">Avg Rating</th>
            <th className="text-left py-2">Sentiment</th>
          </tr>
        </thead>
        <tbody>
          <tr className="border-b">
            <td colSpan={4} className="text-center py-4 text-gray-500">
              No data available
            </td>
          </tr>
        </tbody>
      </table>
    </Card>
  );
};
