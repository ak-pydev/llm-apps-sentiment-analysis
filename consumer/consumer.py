# consumer.py
import os
import json
import time
from datetime import datetime
from kafka import KafkaConsumer
import psycopg2
from psycopg2.extras import execute_values


KAFKA_BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "reviews")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "llm_reviews")
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")


def connect_postgres(retries: int = 5, delay: int = 5):
    """Connect to PostgreSQL with retry logic"""
    for attempt in range(1, retries + 1):
        try:
            print(f"Connecting to PostgreSQL at {POSTGRES_HOST}:{POSTGRES_PORT} (attempt {attempt}/{retries})")
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )
            print("✓ Connected to PostgreSQL!")
            return conn
        except Exception as e:
            print(f"Failed to connect: {e}")
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise


def setup_database(conn):
    """Create table if it doesn't exist"""
    cur = conn.cursor()
    
    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            app_name VARCHAR(255),
            reviewId VARCHAR(255) PRIMARY KEY,
            at TIMESTAMP,
            score DOUBLE PRECISION,
            content TEXT,
            thumbsUpCount INTEGER
        )
    """)
    
    conn.commit()
    cur.close()
    print("✓ PostgreSQL table ready")


def main():
    print("=" * 60)
    print("Kafka to PostgreSQL Consumer")
    print("=" * 60)
    print(f"Kafka Broker: {KAFKA_BROKER}")
    print(f"Topic: {TOPIC}")
    print(f"PostgreSQL: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    print("=" * 60)
    
    # Connect to PostgreSQL
    conn = connect_postgres()
    setup_database(conn)
    
    # Prepare cursor for insertions
    cur = conn.cursor()
    
    # Kafka Consumer
    print("\nConnecting to Kafka...")
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="postgres-consumer-group",
        consumer_timeout_ms=10000,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    
    print("✓ Connected to Kafka")
    print("Listening for messages...\n")
    
    count = 0
    errors = 0
    start_time = time.time()
    
    try:
        for msg in consumer:
            try:
                rec = msg.value
                
                # Extract fields
                app_name = rec.get("app_name", "unknown")
                review_id = rec.get("reviewId", "")
                
                if not review_id:
                    print(f"⚠️  Skipping record with missing reviewId")
                    continue
                
                # Parse timestamp
                at_raw = rec.get("at", "")
                try:
                    if at_raw:
                        at = datetime.fromisoformat(at_raw.replace("Z", "+00:00"))
                    else:
                        at = datetime.now()
                except Exception as e:
                    print(f"Warning: Could not parse timestamp '{at_raw}': {e}")
                    at = datetime.now()
                
                # Parse numeric fields
                try:
                    score = float(rec.get("score", 0))
                except (ValueError, TypeError):
                    score = 0.0
                
                content = rec.get("content", "")
                
                try:
                    thumbs = int(rec.get("thumbsUpCount", 0))
                except (ValueError, TypeError):
                    thumbs = 0
                
                # Insert into PostgreSQL (ON CONFLICT to handle duplicates)
                cur.execute("""
                    INSERT INTO reviews (app_name, reviewId, at, score, content, thumbsUpCount)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (reviewId) DO UPDATE SET
                        app_name = EXCLUDED.app_name,
                        at = EXCLUDED.at,
                        score = EXCLUDED.score,
                        content = EXCLUDED.content,
                        thumbsUpCount = EXCLUDED.thumbsUpCount
                """, (app_name, review_id, at, score, content, thumbs))
                
                conn.commit()
                count += 1
                
                # Progress update
                if count % 100 == 0:
                    elapsed = time.time() - start_time
                    rate = count / elapsed if elapsed > 0 else 0
                    print(f"[{count:,}] Inserted | Rate: {rate:.1f} records/sec | App: {app_name}")
                
            except Exception as e:
                errors += 1
                print(f"✗ Error processing record: {e}")
                conn.rollback()  # Rollback failed transaction
                if errors > 10:
                    print("Too many errors, stopping...")
                    break
    
    except KeyboardInterrupt:
        print("\n\nStopping consumer (Ctrl+C pressed)...")
    
    finally:
        elapsed = time.time() - start_time
        rate = count / elapsed if elapsed > 0 else 0
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total records inserted: {count:,}")
        print(f"Errors encountered: {errors}")
        print(f"Time elapsed: {elapsed:.1f} seconds")
        print(f"Average rate: {rate:.1f} records/sec")
        print("=" * 60)
        
        # Verify data
        if count > 0:
            print("\nVerifying data in PostgreSQL...")
            cur.execute("SELECT COUNT(*) FROM reviews")
            total = cur.fetchone()[0]
            print(f"✓ Total records in PostgreSQL: {total:,}")
            
            # Show sample by app
            print("\nBreakdown by app:")
            cur.execute("""
                SELECT app_name, COUNT(*) as count 
                FROM reviews 
                GROUP BY app_name 
                ORDER BY count DESC
            """)
            for row in cur.fetchall():
                print(f"  {row[0]}: {row[1]:,} reviews")
        
        cur.close()
        conn.close()
        consumer.close()
        print("\n✓ Connections closed")


if __name__ == "__main__":
    main()