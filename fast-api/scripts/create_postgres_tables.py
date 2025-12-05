#!/usr/bin/env python3
"""
Create Postgres database `llm_reviews` and the analytics tables used by the project.

Usage:
  python fast-api/scripts/create_postgres_tables.py

The script connects first to the `postgres` default DB (so it can CREATE DATABASE), then
reconnects to the newly created `llm_reviews` database to create tables.

Environment: Postgres must be reachable at localhost:5432 and accept the credentials
in the script (user/password `airflow` by default). If you're running Postgres via
`docker-compose`, ensure the container is up first.
"""
import psycopg2
from psycopg2 import sql

# Connect to default postgres database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="airflow",
    password="airflow"
)
conn.autocommit = True
cur = conn.cursor()

# Create database
try:
    cur.execute("CREATE DATABASE llm_reviews")
    print("✓ Database created")
except Exception:
    print("Database already exists")

cur.close()
conn.close()

# Connect to new database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="llm_reviews",
    user="airflow",
    password="airflow"
)
cur = conn.cursor()

# Create tables
tables = {
    "reviews": """
        CREATE TABLE IF NOT EXISTS reviews (
            app_name VARCHAR(255),
            reviewId VARCHAR(255) PRIMARY KEY,
            at TIMESTAMP,
            score DOUBLE PRECISION,
            content TEXT,
            thumbsUpCount INTEGER
        )
    """,
    "daily_app_stats": """
        CREATE TABLE IF NOT EXISTS daily_app_stats (
            app_name VARCHAR(255),
            day DATE,
            review_count BIGINT,
            avg_score DOUBLE PRECISION,
            avg_thumbs_up DOUBLE PRECISION,
            PRIMARY KEY (app_name, day)
        )
    """,
    "dashboard_overview": """
        CREATE TABLE IF NOT EXISTS dashboard_overview (
            metric_key VARCHAR(50) PRIMARY KEY,
            total_reviews BIGINT,
            total_apps BIGINT,
            overall_avg_rating DOUBLE PRECISION,
            total_engagement BIGINT,
            updated_at TIMESTAMP
        )
    """,
    "dashboard_rankings": """
        CREATE TABLE IF NOT EXISTS dashboard_rankings (
            app_name VARCHAR(255) PRIMARY KEY,
            total_reviews BIGINT,
            avg_rating DOUBLE PRECISION,
            avg_engagement DOUBLE PRECISION,
            updated_at TIMESTAMP
        )
    """,
    "dashboard_daily_stats": """
        CREATE TABLE IF NOT EXISTS dashboard_daily_stats (
            app_name VARCHAR(255),
            date DATE,
            review_count BIGINT,
            avg_rating DOUBLE PRECISION,
            avg_engagement DOUBLE PRECISION,
            PRIMARY KEY (app_name, date)
        )
    """,
    "dashboard_sentiment_dist": """
        CREATE TABLE IF NOT EXISTS dashboard_sentiment_dist (
            app_name VARCHAR(255),
            sentiment VARCHAR(50),
            count BIGINT,
            PRIMARY KEY (app_name, sentiment)
        )
    """,
    "dashboard_rating_dist": """
        CREATE TABLE IF NOT EXISTS dashboard_rating_dist (
            app_name VARCHAR(255),
            score DOUBLE PRECISION,
            count BIGINT,
            PRIMARY KEY (app_name, score)
        )
    """,
    "dashboard_top_reviews": """
        CREATE TABLE IF NOT EXISTS dashboard_top_reviews (
            reviewId VARCHAR(255) PRIMARY KEY,
            app_name VARCHAR(255),
            content TEXT,
            score DOUBLE PRECISION,
            thumbsUpCount INTEGER,
            at TIMESTAMP
        )
    """,
    "dashboard_trending": """
        CREATE TABLE IF NOT EXISTS dashboard_trending (
            app_name VARCHAR(255) PRIMARY KEY,
            recent_rating DOUBLE PRECISION,
            recent_reviews BIGINT,
            previous_rating DOUBLE PRECISION,
            previous_reviews BIGINT,
            rating_change DOUBLE PRECISION,
            review_growth BIGINT,
            updated_at TIMESTAMP
        )
    """,
    "dashboard_peak_hours": """
        CREATE TABLE IF NOT EXISTS dashboard_peak_hours (
            app_name VARCHAR(255),
            hour INTEGER,
            review_count BIGINT,
            avg_rating DOUBLE PRECISION,
            PRIMARY KEY (app_name, hour)
        )
    """
}

for table_name, sql_text in tables.items():
    cur.execute(sql.SQL(sql_text))
    print(f"✓ Created table: {table_name}")

conn.commit()
cur.close()
conn.close()

print("\n✓ All tables created successfully!")
