#!/bin/bash

echo "Setting up PostgreSQL database and tables..."

# Create database and tables
docker exec -i postgres psql -U airflow < sql/create_tables.sql

# Verify
echo ""
echo "Verifying tables..."
docker exec -it postgres psql -U airflow -d llm_reviews -c "\dt"

echo ""
echo "✓ PostgreSQL setup complete!"