# LLM App Sentiment Analysis Platform

Full-stack web app for analyzing app reviews with sentiment analysis. Built with **FastAPI** (backend), **React** (frontend), **PostgreSQL** (database), **Kafka** & **Spark** (streaming).

## 🚀 Quick Start

### Prerequisites
- Python 3.9+, Node.js 18+, PostgreSQL 13+

### Start Services

```bash
# Terminal 1: Backend
cd fast-api && source venv/bin/activate && pip install -r requirements.txt
uvicorn fast_api.main:app --reload

# Terminal 2: Frontend
cd ui-dashboard && npm install && npm run dev

# Open: http://localhost:5173
```

**API Docs**: http://localhost:8000/docs

---

## 🏗️ Architecture

```
Scraper → Kafka → Spark → PostgreSQL
                              ↓
                       FastAPI Backend (8000)
                              ↓
                       React Frontend (5173)
```

### Database (10 Tables)
- `reviews` - Raw review data
- `daily_app_stats` - Daily aggregates
- `dashboard_*` - Analytics tables (overview, rankings, sentiment, ratings, trending, peak_hours, top_reviews, daily_stats)

### API Endpoints (16 Total)

**Apps** (`/apps`)
- `GET /apps` - List apps
- `GET /apps/{app_name}/reviews` - Get reviews
- `GET /apps/{app_name}/stats` - Get stats
- `GET /apps/{app_name}/daily-stats` - Daily trend
- `GET /apps/{app_name}/sentiment-dist` - Sentiment breakdown
- `GET /apps/{app_name}/rating-dist` - Rating distribution

**Dashboard** (`/dashboard`)
- `GET /dashboard/overview` - Global metrics
- `GET /dashboard/rankings` - App rankings
- `GET /dashboard/daily-stats` - Time-series data
- `GET /dashboard/sentiment-distribution` - Sentiment dist
- `GET /dashboard/rating-distribution` - Rating dist
- `GET /dashboard/top-reviews` - Top positive/negative
- `GET /dashboard/trending` - Trending apps
- `GET /dashboard/peak-hours` - Volume by hour
- `GET /dashboard/full` - Complete snapshot

---

## 📁 Project Structure

```
├── fast-api/              # FastAPI backend
│   ├── db.py             # Database connection
│   ├── models.py         # SQLAlchemy ORM (10 models)
│   ├── schemas.py        # Pydantic schemas
│   ├── main.py           # FastAPI app
│   ├── routers/
│   │   ├── apps.py       # 7 app endpoints
│   │   └── dashboard.py  # 8 dashboard endpoints
│   └── requirements.txt
│
├── ui-dashboard/         # React frontend
│   ├── src/
│   │   ├── components/   # Layout, charts, UI, metrics
│   │   ├── hooks/        # useApps, useAppStats, useDashboardMetrics, useTrending
│   │   ├── pages/        # Dashboard, AppPage, ReviewsPage
│   │   ├── api/          # API client
│   │   └── utils/        # format.ts, colors.ts
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── README.md             # This file
├── SETUP.md              # Detailed setup & troubleshooting
└── ui-dashboard/docs/    # Additional documentation
```

---

## 🛠️ Tech Stack

| Backend | Frontend | Database | DevOps |
|---------|----------|----------|--------|
| FastAPI | React 19+ | PostgreSQL | Kafka |
| SQLAlchemy | TypeScript | asyncpg | Spark |
| asyncpg | Vite | SQLAlchemy | Docker |
| Pydantic | Tailwind CSS | - | - |
| - | React Query | - | - |
| - | Recharts | - | - |

---

## 📖 Setup & Docs

**For detailed setup instructions** → See [SETUP.md](./SETUP.md)

**For more documentation** → See [ui-dashboard/docs/](./ui-dashboard/docs/)
- `INDEX.md` - Master guide
- `QUICK_START.md` - Developer reference
- `DEVELOPMENT_CHECKLIST.md` - Task list

---

## 🔧 Development

### Backend Development
```bash
cd fast-api
source venv/bin/activate
uvicorn fast_api.main:app --reload
# http://localhost:8000/docs
```

### Frontend Development
```bash
cd ui-dashboard
npm run dev
# http://localhost:5173
```

### Production Build
```bash
# Backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker fast_api.main:app

# Frontend
cd ui-dashboard && npm run build
```

---

## ❓ Troubleshooting

| Issue | Fix |
|-------|-----|
| Port in use | `lsof -i :8000` then `kill -9 <PID>` |
| DB connection failed | `brew services start postgresql` |
| CORS error | Check `VITE_API_BASE_URL` in `.env` |
| Modules not found | `npm install` or `pip install -r requirements.txt` |

---

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Vite Guide](https://vitejs.dev/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

---

**License**: MIT | **Status**: Production Ready ✅
