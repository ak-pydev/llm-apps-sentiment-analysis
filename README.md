# LLM App - Sentiment Analysis (example infra)

This repository contains a lightweight example scaffold for a streaming sentiment-analysis pipeline.
It includes components for Kafka, Cassandra, a producer, a Spark streaming job, and an Airflow DAG for daily stats.

Quick structure

- `docker-compose.yml` - orchestrates Kafka, Zookeeper, Cassandra, producer, Spark, and Airflow (example)
- `airflow/` - DAGs and requirements
  - `dags/sentiment_daily_stats.py` - Airflow DAG that queries Cassandra for daily sentiment counts
  - `requirements.txt` - dependencies for Airflow (Cassandra driver)
- `spark/` - Spark job Dockerfile and streaming job
  - `Dockerfile` - builds Spark image (uses bitnami/spark base)
  - `sentiment_streaming_job.py` - PySpark Structured Streaming job that reads Kafka and computes sentiment
- `producer/` - simple Python Kafka producer
  - `Dockerfile` - builds minimal producer image
  - `producer.py` - emits sample messages to `sentiment` topic
- `cassandra/init.cql` - creates keyspace/table on Cassandra init
- `config/kafka_topics.sh` - helper to create a Kafka topic

Run (local dev)

1. Start services (requires Docker & Docker Compose):

```bash
docker-compose up --build
```

2. Create the Kafka topic (if needed):

```bash
./config/kafka_topics.sh
```

3. The `producer` service in compose will emit sample messages to the `sentiment` topic. The Spark service runs a demo `spark-submit` that prints sentiment to console. Airflow UI is available at `http://localhost:8080` (webserver image used in compose).

Notes

- This scaffold is intended as an example; images, versions, and production hardening are intentionally minimal.
- For real deployments: secure credentials, use proper Docker images for Spark/airflow, externalize configs, and use a proper cluster for Spark and Cassandra.
