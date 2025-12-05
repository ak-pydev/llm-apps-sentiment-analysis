import React from 'react';

interface ErrorProps {
  message: string;
  onRetry?: () => void;
}

export const Error: React.FC<ErrorProps> = ({ message, onRetry }) => {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <p className="text-red-800 font-semibold">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 text-red-600 hover:text-red-800 underline"
        >
          Retry
        </button>
      )}
    </div>
  );
};
