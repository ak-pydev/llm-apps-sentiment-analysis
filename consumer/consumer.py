import os
import json
import time
from datetime import datetime

from kafka import KafkaConsumer
from cassandra.cluster import Cluster

KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "reviews")

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "llm_reviews")


def connect_cassandra(host: str, port: int, retries: int = 5, delay: int = 3):
    for attempt in range(1, retries + 1):
        try:
            print(f"Connecting to Cassandra at {host}:{port} (attempt {attempt}/{retries})")
            cluster = Cluster([host], port=port)
            session = cluster.connect()
            return cluster, session
        except Exception as e:
            print(f"Failed to connect to Cassandra: {e}")
            if attempt == retries:
                raise
            time.sleep(delay)


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=None,
    consumer_timeout_ms=5000,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print("Starting consumer...")

cluster, session = connect_cassandra(CASSANDRA_HOST, CASSANDRA_PORT)

session.execute(
    f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH replication = {{'class':'SimpleStrategy', 'replication_factor':1}}
"""
)
session.set_keyspace(KEYSPACE)
session.execute(
    """
    CREATE TABLE IF NOT EXISTS reviews_by_app (
        app_name text,
        reviewId text,
        at timestamp,
        score double,
        content text,
        thumbsUpCount int,
        PRIMARY KEY ((app_name), reviewId, at)
    )
"""
)

print("Cassandra keyspace/table ready.")

insert_cql = session.prepare(
    """
    INSERT INTO reviews_by_app (app_name, reviewId, at, score, content, thumbsUpCount)
    VALUES (?, ?, ?, ?, ?, ?)
"""
)

count = 0

for msg in consumer:
    rec = msg.value
    print("Consumed:", rec)

    app_name = rec.get("app_name")
    review_id = rec.get("reviewId")
    at_raw = rec.get("at")

    at = None
    if at_raw:
        try:
            at = datetime.fromisoformat(at_raw.replace("Z", "+00:00"))
        except Exception:
            at = None

    score = float(rec.get("score")) if rec.get("score") is not None else None
    content = rec.get("content")
    thumbs = int(rec.get("thumbsUpCount")) if rec.get("thumbsUpCount") is not None else None

    try:
        session.execute(insert_cql, (app_name, review_id, at, score, content, thumbs))
        print(f"Inserted reviewId={review_id} for app={app_name}")
    except Exception as e:
        print("Error inserting record:", e, rec)

    count += 1
    time.sleep(3)

if count == 0:
    print("No messages consumed. Exiting.")

consumer.close()
cluster.shutdown()
