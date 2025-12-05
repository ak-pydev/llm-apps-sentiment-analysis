# LLM App Sentiment Analysis - Setup Guide

**📖 For more docs** → See [`ui-dashboard/docs/`](./ui-dashboard/docs/)

This guide walks you through setting up and running the complete full-stack LLM App Review Analytics Platform.

## Prerequisites

Before starting, ensure you have:
- **Python 3.9+** installed
- **Node.js 18+** and npm installed
- **PostgreSQL 13+** running locally
- **Git** for version control

## Step 1: Database Setup

### Create PostgreSQL Database

```bash
# Connect to PostgreSQL (default: postgres user)
psql -U postgres

# In psql shell, create the database:
CREATE DATABASE llm_reviews;

# Exit psql
\q
```

Alternatively, if you have a password:
```bash
psql -U postgres -h localhost -d postgres -c "CREATE DATABASE llm_reviews;"
```

### Run Database Migrations

The FastAPI application will initialize the database schema on first run with SQLAlchemy ORM. Ensure your database is running before starting the backend.

## Step 2: Backend Setup (FastAPI)

### Install Dependencies

```bash
# Navigate to the backend directory
cd fast-api

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if needed (default values should work for local development)
# Key variables:
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/llm_reviews
# API_HOST=0.0.0.0
# API_PORT=8000
```

### Start the Backend Server

```bash
# From the fast-api directory with venv activated:
uvicorn fast_api.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Access API Documentation

- **Interactive Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Step 3: Frontend Setup (React + TypeScript)

### Install Dependencies

```bash
# Navigate to the frontend directory
cd ui-dashboard

# Install Node dependencies
npm install
```

### Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if needed
# Key variable:
# VITE_API_BASE_URL=http://localhost:8000
```

### Start the Development Server

```bash
# From the ui-dashboard directory:
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

### Access the Dashboard

Open your browser to: http://localhost:5173/

## Project Structure

```
llm-app-sentiment-analysis/
├── fast-api/
│   ├── db.py                 # Database connection & session management
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic response schemas
│   ├── main.py               # FastAPI application entry point
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── apps.py           # App-specific endpoints
│   │   └── dashboard.py      # Dashboard analytics endpoints
│   ├── requirements.txt
│   ├── .env.example
│   └── venv/                 # Python virtual environment (created during setup)
│
├── ui-dashboard/
│   ├── src/
│   │   ├── api/              # API client functions
│   │   ├── components/       # React components
│   │   │   ├── layout/       # Layout components
│   │   │   ├── charts/       # Chart visualizations
│   │   │   ├── ui/           # Base UI components
│   │   │   └── metrics/      # Metric display components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── pages/            # Page components
│   │   ├── utils/            # Utility functions
│   │   ├── App.tsx           # Main app component
│   │   └── main.tsx          # React entry point
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   ├── .env.example
│   └── node_modules/         # Node dependencies (created during setup)
│
├── docker-compose.yml
├── README.md
└── SETUP.md (this file)
```

## API Endpoints Reference

### Apps Endpoints (`/apps`)

- `GET /apps` - List all apps
- `GET /apps/{app_name}/reviews` - Get reviews for app (with pagination)
- `GET /apps/{app_name}/stats` - Get aggregated stats
- `GET /apps/{app_name}/daily-stats` - Get daily trend data
- `GET /apps/{app_name}/sentiment-dist` - Get sentiment breakdown
- `GET /apps/{app_name}/rating-dist` - Get rating distribution

### Dashboard Endpoints (`/dashboard`)

- `GET /dashboard/overview` - Global metrics overview
- `GET /dashboard/rankings` - App rankings
- `GET /dashboard/daily-stats` - Time-series data
- `GET /dashboard/sentiment-distribution` - Sentiment distribution
- `GET /dashboard/rating-distribution` - Rating distribution
- `GET /dashboard/top-reviews` - Top positive/negative reviews
- `GET /dashboard/trending` - Trending apps
- `GET /dashboard/peak-hours` - Review volume by hour
- `GET /dashboard/full` - Complete dashboard snapshot

## Frontend Pages

- **Dashboard** (`/`) - Overview with metrics, charts, and rankings
- **Apps** (`/apps`) - List of all apps with review counts
- **Reviews** (`/reviews`) - Top positive and negative reviews

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port:
uvicorn fast_api.main:app --reload --port 8001
```

**Database connection failed:**
- Ensure PostgreSQL is running: `brew services start postgresql` (macOS)
- Check DATABASE_URL in `.env`
- Verify database exists: `psql -U postgres -l`

**Import errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Frontend Issues

**Port 5173 already in use:**
```bash
npm run dev -- --port 5174
```

**API connection errors:**
- Check VITE_API_BASE_URL in `.env`
- Ensure backend is running on port 8000
- Check browser console for CORS errors

**Module not found errors:**
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`

## Development Workflow

### 1. Terminal 1: Backend

```bash
cd fast-api
source venv/bin/activate
uvicorn fast_api.main:app --reload
```

### 2. Terminal 2: Frontend

```bash
cd ui-dashboard
npm run dev
```

### 3. Browser

Open http://localhost:5173/

## Building for Production

### Backend

```bash
cd fast-api
# Install production dependencies
pip install -r requirements.txt

# Run with Gunicorn for production
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker fast_api.main:app --bind 0.0.0.0:8000
```

### Frontend

```bash
cd ui-dashboard
npm run build

# Output is in ui-dashboard/dist/
# Serve with any static file server or integrate with backend
```

## Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Database Schema Overview

### Core Tables

- **reviews** - Raw review data (app_name, rating, sentiment, text, timestamps)
- **daily_app_stats** - Daily aggregates per app

### Dashboard Tables

- **dashboard_overview** - Global metrics
- **dashboard_rankings** - App rankings
- **dashboard_daily_stats** - Time-series data
- **dashboard_sentiment_dist** - Sentiment breakdown
- **dashboard_rating_dist** - Rating distribution
- **dashboard_top_reviews** - Best/worst reviews
- **dashboard_trending** - Trending apps
- **dashboard_peak_hours** - Review volume by hour

## Performance Tips

1. **Pagination**: Use `limit` and `offset` on review endpoints
2. **Caching**: Implement React Query's stale-while-revalidate strategy
3. **Database**: Ensure indexes are created (automatically done by ORM)
4. **Frontend**: Use React.lazy() for code splitting
5. **API**: Limit date ranges for historical queries

## Next Steps

1. **Data Population**: Populate the database with your review data
2. **Monitoring**: Set up logging and monitoring
3. **Authentication**: Add authentication layer if needed
4. **Deployment**: Deploy to your cloud platform (AWS, Azure, GCP)
5. **Styling**: Customize TailwindCSS and ShadCN UI themes

## Support & Documentation

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy Async**: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- **React**: https://react.dev/
- **Vite**: https://vitejs.dev/
- **TailwindCSS**: https://tailwindcss.com/
- **Recharts**: https://recharts.org/

## License

MIT License - Feel free to use this template for your projects!
