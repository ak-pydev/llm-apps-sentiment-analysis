# Developer Quick Reference

## 🚀 Start Development (Copy & Paste)

### Terminal 1 - Backend
```bash
cd fast-api
source venv/bin/activate  # or: . venv/bin/activate
uvicorn fast_api.main:app --reload
```
➜ Opens: http://localhost:8000/docs (Swagger UI)

### Terminal 2 - Frontend
```bash
cd ui-dashboard
npm run dev
```
➜ Opens: http://localhost:5173

### Terminal 3 - Database (Optional)
```bash
psql -U postgres -d llm_reviews
```

## 📋 File Locations

| Purpose | File |
|---------|------|
| Database Connection | `fast-api/db.py` |
| ORM Models | `fast-api/models.py` |
| API Schemas | `fast-api/schemas.py` |
| Main App | `fast-api/main.py` |
| App Routes | `fast-api/routers/apps.py` |
| Dashboard Routes | `fast-api/routers/dashboard.py` |
| React Hooks | `ui-dashboard/src/hooks/` |
| Components | `ui-dashboard/src/components/` |
| Pages | `ui-dashboard/src/pages/` |
| API Client | `ui-dashboard/src/api/` |

## 🔌 API Endpoints

### List All Apps
```
GET http://localhost:8000/apps
```

### Get App Reviews
```
GET http://localhost:8000/apps/{app_name}/reviews?limit=50&offset=0
```

### Get Dashboard Overview
```
GET http://localhost:8000/dashboard/overview
```

### Get Dashboard Full Snapshot
```
GET http://localhost:8000/dashboard/full
```

See [SETUP.md](./SETUP.md) for complete endpoint reference.

## 🛠️ Common Commands

### Backend
```bash
# Activate venv
source fast-api/venv/bin/activate

# Install dependencies
pip install -r fast-api/requirements.txt

# Run with auto-reload
uvicorn fast_api.main:app --reload

# Run on different port
uvicorn fast_api.main:app --port 8001

# View API docs
# Browser: http://localhost:8000/docs
```

### Frontend
```bash
cd ui-dashboard

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview build
npm run preview

# Lint code
npm run lint
```

### Database
```bash
# Connect to database
psql -U postgres -d llm_reviews

# List all tables
\dt

# Check specific table
SELECT * FROM reviews LIMIT 5;

# Exit
\q
```

## 🔗 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | React Dashboard |
| Backend | http://localhost:8000 | FastAPI Server |
| API Docs | http://localhost:8000/docs | Interactive Swagger |
| API ReDoc | http://localhost:8000/redoc | Alternative API Docs |
| Health Check | http://localhost:8000/health | Server Status |
| Database | localhost:5432 | PostgreSQL (psql) |

## 📦 Dependencies

### Backend
```
fastapi==0.104.1         # Web framework
uvicorn[standard]==0.24.0 # ASGI server
sqlalchemy==2.0.23        # ORM
asyncpg==0.29.0           # Async PostgreSQL
pydantic==2.5.0           # Data validation
```

### Frontend
```
react@^18                 # UI framework
typescript~5.9            # Type safety
vite@^7                   # Build tool
tailwindcss@^4            # Styling
react-query@^5            # Data fetching (from @tanstack/react-query)
recharts@^3               # Charting
axios@^1                  # HTTP client
```

## 🐛 Troubleshooting Quick Fixes

### Port Already in Use
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database Connection Failed
```bash
# Start PostgreSQL
brew services start postgresql

# Or connect with password
psql -U postgres -h localhost
```

### CORS Error
Check `ALLOWED_ORIGINS` in `fast-api/.env`:
```
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:8000
```

### Module Not Found
```bash
# Backend
cd fast-api && pip install -r requirements.txt

# Frontend
cd ui-dashboard && rm -rf node_modules && npm install
```

### Vite Build Error
```bash
# Clear cache
rm -rf ui-dashboard/node_modules/.vite

# Reinstall
cd ui-dashboard && npm install
```

## 🎯 Next Steps

After starting both services:

1. **Add Data** - Populate database with review data
2. **Test Endpoints** - Visit http://localhost:8000/docs
3. **Check Frontend** - Visit http://localhost:5173
4. **Integrate React Query** - Update hooks to use `useQuery` pattern
5. **Add Recharts** - Implement actual chart visualizations
6. **Style Components** - Integrate ShadCN/UI components

## 📚 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Vite Guide](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Recharts](https://recharts.org/)

## 💡 Pro Tips

1. **Hot Reload**: Backend reloads on file save (with `--reload`), frontend auto-refreshes
2. **API Testing**: Use Swagger UI at `/docs` instead of Postman
3. **Database Inspection**: Use `psql` CLI or pgAdmin UI
4. **Component Reuse**: Check existing components before creating new ones
5. **Type Safety**: Always export types from schemas/models

## 🔐 Important Files (Don't Commit)

```
.env           # Local environment variables
.env.local     # Local overrides
venv/          # Python virtual environment
node_modules/  # Node packages
dist/          # Build output
```

These are already in `.gitignore`

---

**Last Updated**: Now | **Status**: Ready for Development
