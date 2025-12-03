import os
import json
import time
from datetime import datetime

from kafka import KafkaConsumer
from cassandra.cluster import Cluster


# --------------------
# Config
# --------------------
KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "reviews")

# Host is your Mac, mapped to the cassandra container
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "llm_reviews")


# --------------------
# Helpers
# --------------------
def connect_cassandra(host: str, port: int, delay: int = 5):
    """
    Keep retrying until Cassandra is ready.
    """
    while True:
        try:
            print(f"[CASSANDRA] Connecting to {host}:{port} ...")
            cluster = Cluster([host], port=port)
            session = cluster.connect()
            print("[CASSANDRA] Connected.")
            return cluster, session
        except Exception as e:
            print(f"[CASSANDRA] Not ready: {e}. Retrying in {delay}s...")
            time.sleep(delay)


def parse_timestamp(at_raw: str):
    if not at_raw:
        return None
    try:
        # Handle formats like "2024-01-01T12:34:56Z"
        return datetime.fromisoformat(at_raw.replace("Z", "+00:00"))
    except Exception:
        return None


def to_float(value):
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def to_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        return None


# --------------------
# Kafka Consumer
# --------------------
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=None,  # always read full topic
    consumer_timeout_ms=30000,  # stop after 30s of no messages
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print(f"[KAFKA] Connected to {KAFKA_BROKER}, subscribed to topic: {TOPIC}")


# --------------------
# Cassandra Setup
# --------------------
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

print(f"[CASSANDRA] Keyspace '{KEYSPACE}' and table 'reviews_by_app' are ready.")

insert_cql = session.prepare(
    """
    INSERT INTO reviews_by_app (app_name, reviewId, at, score, content, thumbsUpCount)
    VALUES (?, ?, ?, ?, ?, ?)
"""
)


# --------------------
# Consume & Insert Loop
# --------------------
count = 0
print("[CONSUMER] Starting main loop...")

for msg in consumer:
    rec = msg.value
    print("[KAFKA] Consumed:", rec)

    app_name = rec.get("app_name")
    review_id = rec.get("reviewId")
    at = parse_timestamp(rec.get("at"))
    score = to_float(rec.get("score"))
    content = rec.get("content")
    thumbs = to_int(rec.get("thumbsUpCount"))

    try:
        session.execute(
            insert_cql,
            (app_name, review_id, at, score, content, thumbs),
        )
        print(f"[CASSANDRA] Inserted reviewId={review_id} for app={app_name}")
    except Exception as e:
        print("[CASSANDRA] Error inserting record:", e)
        print("  Record:", rec)

    count += 1
    time.sleep(3)  # throttle for readability

if count == 0:
    print("[CONSUMER] No messages consumed. Exiting.")

consumer.close()
cluster.shutdown()
print(f"[CONSUMER] Done. Total messages inserted: {count}")
