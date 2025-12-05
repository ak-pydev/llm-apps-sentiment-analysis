# Spark Jobs

Two batch processing jobs that transform and aggregate review data for analytics.

---

## `batch_aggregates.py`

**Purpose:** Daily statistics and aggregations from raw reviews.

### What It Does
1. Reads raw reviews from PostgreSQL
2. Groups by app and date
3. Computes:
   - Total review count per app per day
   - Average sentiment score
   - Sentiment distribution (positive/negative/neutral counts)
   - Average rating
4. Stores results in `daily_app_stats` table

### Input
- `reviews` table (raw data from Kafka consumer)

### Output
- `daily_app_stats` table (daily rollups by app)

### Run
```bash
./scripts/helper_script.sh batch_aggregates.py
```

### Environment
```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=llm_reviews
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
```

---

## `dashboard_metric.py`

**Purpose:** Real-time dashboard metrics for UI visualization.

### What It Does
1. Reads from `daily_app_stats` and `reviews` tables
2. Computes multiple materialized views:
   - **dashboard_overview** – Total stats across all apps
   - **dashboard_rankings** – Apps ranked by reviews/rating
   - **dashboard_daily_stats** – Time-series data
   - **dashboard_sentiment_dist** – Sentiment breakdown
   - **dashboard_rating_dist** – Rating distribution
   - **dashboard_top_reviews** – Best/worst reviews
   - **dashboard_trending** – Trending topics
   - **dashboard_peak_hours** – Activity by time

3. Stores results in 8 dashboard tables

### Input
- `daily_app_stats` (from batch_aggregates)
- `reviews` (raw consumer data)

### Output
- 8 dashboard tables (read by API/UI)

### Run
```bash
./scripts/helper_script.sh dashboard_metric.py
```

### Environment
Same as `batch_aggregates.py`

---

## How They Work Together

```
Consumer writes → reviews (PostgreSQL)
                      ↓
batch_aggregates.py → daily_app_stats (rollups)
                      ↓
dashboard_metric.py → 8 dashboard tables → API/UI
```

1. **Consumer** populates raw `reviews` table (streaming)
2. **batch_aggregates** computes daily stats (daily scheduled)
3. **dashboard_metric** creates dashboard tables (real-time scheduled)

---

## Running Locally

```bash
# Ensure PostgreSQL is running
docker compose up -d postgres

# Set environment variables
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=llm_reviews
export POSTGRES_USER=airflow
export POSTGRES_PASSWORD=airflow

# Run batch job
python spark-jobs/batch_aggregates.py

# Run dashboard job
python spark-jobs/dashboard_metric.py
```

---

## Debugging

### Check PostgreSQL Connection
```bash
psql -h localhost -U airflow -d llm_reviews -c "\dt"
```

### View Spark Logs
```bash
./scripts/helper_script.sh batch_aggregates.py | tail -100
```

### Query Results
```bash
docker exec -it postgres psql -U airflow -d llm_reviews
SELECT * FROM daily_app_stats LIMIT 10;
SELECT * FROM dashboard_rankings LIMIT 10;
```

---

**Author:** ak-pydev
