/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        positive: '#10b981',
        negative: '#ef4444',
        neutral: '#6b7280',
        sentiment: {
          positive: '#10b981',
          negative: '#ef4444',
          neutral: '#6b7280',
        },
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
      },
    },
  },
  plugins: [],
}
