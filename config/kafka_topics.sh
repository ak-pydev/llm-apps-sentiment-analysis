#!/usr/bin/env bash
set -euo pipefail

# Simple helper to create a Kafka topic named 'sentiment'.
# Adjust KAFKA_BIN and BOOTSTRAP if your environment differs.

KAFKA_BIN=${KAFKA_BIN:-/usr/bin}
BOOTSTRAP=${BOOTSTRAP:-localhost:9092}
TOPIC=${TOPIC:-sentiment}

if command -v kafka-topics.sh >/dev/null 2>&1; then
  kafka-topics.sh --create --topic "$TOPIC" --bootstrap-server "$BOOTSTRAP" --partitions 1 --replication-factor 1 || true
else
  echo "kafka-topics.sh not found; ensure Kafka binaries are installed or use your platform tooling to create topics"
fi
