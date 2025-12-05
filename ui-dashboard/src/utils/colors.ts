export const sentimentColors = {
  positive: '#10b981', // emerald
  negative: '#ef4444', // red
  neutral: '#6b7280', // gray
};

export const ratingColors = (rating: number): string => {
  if (rating >= 4) return '#10b981'; // green
  if (rating >= 3) return '#f59e0b'; // amber
  if (rating >= 2) return '#f97316'; // orange
  return '#ef4444'; // red
};

export const chartColors = [
  '#3b82f6', // blue
  '#10b981', // green
  '#f59e0b', // amber
  '#ef4444', // red
  '#8b5cf6', // purple
  '#ec4899', // pink
];
