#!/bin/bash

# Usage: ./scripts/helper_script.sh batch_aggregates.py
# Usage: ./scripts/helper_script.sh dashboard_metric.py

if [ -z "$1" ]; then
  echo " Error: No script name provided"
  echo ""
  echo "Usage: ./scripts/helper_script.sh <script_name>"
  echo ""
  echo "Examples:"
  echo "  ./scripts/helper_script.sh batch_aggregates.py"
  echo "  ./scripts/helper_script.sh dashboard_metric.py"
  exit 1
fi

SCRIPT_NAME=$1

echo "=========================================="
echo "Running Spark Job: $SCRIPT_NAME"
echo "=========================================="

# Ensure Ivy cache directory exists with proper permissions (run as root)
echo "Setting up Ivy cache..."
docker exec -u root spark-master bash -c "mkdir -p /tmp/.ivy2/cache && chown -R spark:spark /tmp/.ivy2 && chmod -R 777 /tmp/.ivy2" 2>/dev/null

# Run Spark job
docker exec -it spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --packages org.postgresql:postgresql:42.6.0 \
  --conf spark.jars.ivy=/tmp/.ivy2 \
  /opt/spark-jobs/$SCRIPT_NAME

if [ $? -eq 0 ]; then
  echo ""
  echo " Job completed successfully!"
else
  echo ""
  echo " Job failed!"
  exit 1
fi