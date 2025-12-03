import os
import glob
import csv
import json
import time
from kafka import KafkaProducer

BROKER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "reviews")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

data_dir = "data/raw"
csv_files = glob.glob(os.path.join(data_dir, "*_reviews.csv"))

for csv_path in csv_files:
    app_name = os.path.basename(csv_path).split("_reviews.csv")[0]
    print(f"\n>>> Producing reviews for app: {app_name} from {csv_path}")
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["app_name"] = app_name
            # Log to CLI
            print("Sending:", row)
            producer.send(TOPIC, row)
            time.sleep(2)  

producer.flush()
producer.close()
print("\nAll messages sent.")
