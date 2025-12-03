#!/bin/bash

# Usage: ./kafka-topic.sh <topic_name>
# Example: ./kafka-topic.sh reviews

BOOTSTRAP_SERVER="localhost:9092"
TOPIC_NAME="${1:-reviews}"

docker exec -it kafka kafka-topics.sh \
  --bootstrap-server $BOOTSTRAP_SERVER \
  --create \
  --topic "$TOPIC_NAME" \
  --partitions 1 \
  --replication-factor 1

docker exec -it kafka kafka-topics.sh \
  --bootstrap-server $BOOTSTRAP_SERVER \
  --list
