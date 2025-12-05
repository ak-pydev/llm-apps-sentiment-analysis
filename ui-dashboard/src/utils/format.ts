export const formatNumber = (num: number): string => {
  return new Intl.NumberFormat().format(num);
};

export const formatPercent = (num: number): string => {
  return `${(num * 100).toFixed(1)}%`;
};

export const formatDate = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const truncate = (str: string, length: number): string => {
  return str.length > length ? str.substring(0, length) + '...' : str;
};
