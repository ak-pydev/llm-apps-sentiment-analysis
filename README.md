# Sentiment Analysis Data Pipeline

A modern streaming pipeline for app review sentiment analysis built with **Kafka**, **Spark**, **Cassandra**, and **Airflow**.

```
Scraper → Kafka → Spark → Cassandra → API / Dashboard / Notebook
↑ Airflow scheduling & orchestration
```

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local development)

### Setup (5 minutes)

```bash
# 1. Start all services
docker compose up -d

# 2. Verify services are running
docker compose ps

# 3. Run the scraper (streams app reviews to Kafka)
uv run python producer/producer.py

# 4. In another terminal, consume & process messages
uv run python consumer/consumer.py
```

**Access UIs:**
- **Spark Master:** http://localhost:8080
- **Airflow:** http://localhost:8082 (find credentials in logs)
- **Cassandra:** Port 9042 (CQL queries via `docker exec`)

---

## Architecture

| Service | Port | Purpose |
|---------|------|---------|
| Zookeeper | 2181 | Kafka coordination |
| Kafka | 9092 | Message broker |
| Cassandra | 9042 | Time-series database |
| Spark Master | 7077, 8080 | Distributed compute & UI |
| PostgreSQL | 5432 | Airflow metadata store |
| Airflow | 8082 | Workflow orchestration |

---

## Project Structure

```
.
├── docker-compose.yml              # Service orchestration
├── data/raw/                       # Input app reviews
├── producer/
│   ├── Dockerfile                  
│   └── producer.py                 # Scraper → Kafka
├── consumer/
│   └── consumer.py                 # Kafka → Process
├── spark/
│   └── Dockerfile                  
├── dags/
│   └── sentiment_daily_stats.py    # Airflow DAG
├── config/
│   └── kafka_topics.sh             
├── airflow/
│   └── requirements.txt            
└── README.md
```

---

## Key Components

### Scraper
- Reads app reviews from data sources
- Streams to Kafka `reviews` topic
- Adds app metadata

**Env vars:**
- `KAFKA_BOOTSTRAP_SERVERS` (default: `localhost:9092`)
- `KAFKA_TOPIC` (default: `reviews`)

### Kafka
- Event broker for review stream
- Decouples scraper from processing
- Enables horizontal scaling

### Spark
- Stream processing engine
- Computes sentiment analysis
- Writes results to Cassandra

### Cassandra
- **Keyspace:** `llm_reviews`
- **Table:** `reviews_by_app`
- Time-series storage for queries

### Airflow
- Schedules scraper runs
- Orchestrates batch aggregations
- Monitors pipeline health

### Outputs
- **API** – Real-time sentiment endpoints
- **Dashboard** – Visualization layer (Grafana/Dash)
- **Notebook** – Analysis & exploration

---

## Commands

### Pipeline

```bash
# Start services (background)
docker compose up -d

# View running services
docker compose ps

# Stream logs (follow mode, last 50 lines)
docker compose logs -f <service> --tail 50

# Stop all services
docker compose down

# Stop and delete volumes (WARNING: destroys data)
docker compose down -v
```

### Kafka

```bash
# List topics
docker exec -it kafka kafka-topics.sh --bootstrap-server kafka:9092 --list

# Create topic
docker exec -it kafka kafka-topics.sh \
  --bootstrap-server kafka:9092 \
  --create --topic reviews --partitions 1 --replication-factor 1

# Consume from beginning
docker exec -it kafka kafka-console-consumer.sh \
  --bootstrap-server kafka:9092 \
  --topic reviews \
  --from-beginning

# Produce test message (interactive)
docker exec -it kafka kafka-console-producer.sh \
  --broker-list kafka:9092 \
  --topic reviews
```

### Producer

```bash
# Run with uv
uv run python producer/producer.py

# Or with Python
python producer/producer.py
```

Scrapes app reviews and streams to Kafka.

### Consumer

```bash
# Run with uv
uv run python consumer/consumer.py

# Or with Python
python consumer/consumer.py
```

Consumes reviews from Kafka, processes them, and writes to Cassandra.

### Cassandra

```bash
# Enter Cassandra shell
docker exec -it cassandra cqlsh

# Inside cqlsh:
DESCRIBE KEYSPACES;
USE llm_reviews;
SELECT * FROM reviews_by_app LIMIT 20;
SELECT COUNT(*) FROM reviews_by_app;
```

### Airflow

**Web UI:** http://localhost:8082

```bash
# Get auto-generated credentials
docker logs airflow | grep -i "username" -n10

# Restart Airflow
docker compose restart airflow

# Manually trigger DAG
docker exec -it airflow airflow dags trigger sentiment_daily_stats

# View task logs
docker exec -it airflow airflow tasks logs sentiment_daily_stats query_cassandra
```

### Spark

**Web UI:** http://localhost:8080

```bash
# Check version
docker exec -it spark-master /opt/spark/bin/spark-submit --version

# Submit job
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /path/to/job.py

# View logs
docker compose logs -f spark-master
```

---

## Local Development

### Setup Python Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r airflow/requirements.txt
```

### Run Airflow Locally

```bash
# Terminal 1
airflow db migrate
airflow webserver

# Terminal 2
airflow scheduler
```

---

## Configuration

### Spark Workers

Adjust in `docker-compose.yml`:

```yaml
spark-worker:
  environment:
    SPARK_WORKER_CORES: 4
    SPARK_WORKER_MEMORY: 4g
```

### Kafka Topics

Edit `config/kafka_topics.sh` or run:

```bash
./config/kafka_topics.sh
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port in use** | Change port in `docker-compose.yml` |
| **Cassandra won't start** | Check `/var/lib/cassandra` permissions |
| **Airflow DB error** | Remove `airflow/airflow.db` and restart |
| **Kafka connection refused** | Verify Kafka running: `docker compose logs kafka` |
| **Services slow to start** | Wait 30s, then check: `docker compose ps` |

---

## Next Steps

- [ ] Add sentiment models (TextBlob, Hugging Face, LLM) to Spark
- [ ] Build API endpoints for sentiment queries
- [ ] Create Grafana dashboard for real-time monitoring
- [ ] Add Jupyter notebook for exploratory analysis
- [ ] Implement schema registry for Kafka
- [ ] Add data quality & validation checks
- [ ] Deploy to production (Kubernetes, cloud)

---

## Resources

- [Apache Kafka Docs](https://kafka.apache.org/documentation/)
- [PySpark Streaming](https://spark.apache.org/docs/latest/streaming-programming-guide.html)
- [Cassandra CQL](https://cassandra.apache.org/doc/latest/cassandra/cql/)
- [Airflow DAGs](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)

---

**License:** MIT  
**Author:** ak-pydev  
**Last Updated:** December 2025
