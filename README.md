# Sentiment Analysis Data Pipeline

A streaming pipeline for app review sentiment analysis: **Scraper → Kafka → Spark → PostgreSQL → Dashboard**.

```
Scraper → Kafka → Spark → PostgreSQL → API / Dashboard / Notebook
                    ↑ Airflow scheduling
```

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+

### Run Pipeline (7 steps)

```bash
# 1. Start services (wait 30s)
docker compose up -d

# 2. Setup database
./scripts/setup_postgres.sh

# 3. Run scraper
python producer/producer.py

# 4. Run consumer
uv run python consumer/consumer.py
# Press Ctrl+C when done

# 5. Batch aggregates
./scripts/helper_script.sh batch_aggregates.py

# 6. Dashboard metrics
./scripts/helper_script.sh dashboard_metric.py

# 7. View results
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT * FROM dashboard_rankings;"
```

**Dashboards:**
- pgAdmin: http://localhost:5050
- Spark UI: http://localhost:8080
- Airflow: http://localhost:8082

---

## Services

| Service | Port | Role |
|---------|------|------|
| Kafka | 9092 | Event broker |
| PostgreSQL | 5432 | Results store |
| Cassandra | 9042 | (optional) |
| Spark | 8080 | Processing |
| Airflow | 8082 | Orchestration |
| pgAdmin | 5050 | DB UI |

---

## Pipeline Steps Explained

1. **Scraper** (`producer/producer.py`) – Reads app reviews, sends to Kafka
2. **Consumer** (`consumer/consumer.py`) – Consumes Kafka messages, processes, stores in PostgreSQL
3. **Batch Aggregates** (`spark-jobs/batch_aggregates.py`) – Daily stats & rollups
4. **Dashboard Metrics** (`spark-jobs/dashboard_metric.py`) – Real-time dashboard data

See [`spark-jobs/README.md`](./spark-jobs/README.md) for details on Spark jobs.

---

## One-Liner (After Setup)

```bash
python producer/producer.py && uv run python consumer/consumer.py & sleep 10 && ./scripts/helper_script.sh batch_aggregates.py && ./scripts/helper_script.sh dashboard_metric.py
```

## Fresh Start (Clear Data)

```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "TRUNCATE TABLE reviews, daily_app_stats, dashboard_overview, dashboard_rankings, dashboard_daily_stats, dashboard_sentiment_dist, dashboard_rating_dist, dashboard_top_reviews, dashboard_trending, dashboard_peak_hours CASCADE;"

# Then re-run steps 3-6 above
```

---

## Commands

### Kafka

```bash
docker exec -it kafka kafka-topics.sh --bootstrap-server kafka:9092 --list
docker exec -it kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic reviews --from-beginning
```

### PostgreSQL

```bash
docker exec -it postgres psql -U airflow -d llm_reviews
```

### Logs

```bash
docker compose logs -f <service>
```

### Stop Services

```bash
docker compose down
docker compose down -v  # delete volumes
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port in use | Modify `docker-compose.yml` |
| Kafka won't start | Check `docker compose logs kafka` |
| DB connection error | Verify PostgreSQL is running & healthy |
| Spark job fails | Check `./scripts/helper_script.sh` output |

---

**License:** MIT | **Author:** ak-pydev
