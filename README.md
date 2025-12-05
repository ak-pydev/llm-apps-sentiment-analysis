# LLM App Sentiment Analysis Pipeline - Execution Commands

## 📋 Prerequisites

- Docker & Docker Compose installed
- Python 3.11+ installed
- Git installed

---

## 🚀 Complete Setup & Execution

### **Step 1: Clone Repository**

```
git clone https://github.com/ak-pydev/llm-apps-sentiment-analysis.git
```
```bash
cd llm-app-sentiment-analysis
```

### **Step 2: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 3: Start All Docker Services**
```bash
docker-compose up -d
```
```bash
sleep 30
```

### **Step 4: Verify Services Are Running**
```bash
docker-compose ps
```

### **Step 5: Setup PostgreSQL Database & Tables**
```bash
chmod +x scripts/setup_postgres.sh
```
```bash
./scripts/setup_postgres.sh
```

### **Step 6: Verify Database & Tables Created**
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "\dt"
```

### **Step 7: Run Producer (Send CSV Data to Kafka)**
```bash
python producer/producer.py
```

### **Step 8: Run Consumer (Kafka → PostgreSQL)**
```bash
python consumer/consumer.py
```
*Press `Ctrl+C` after all messages consumed*

### **Step 9: Verify Data in PostgreSQL**
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT COUNT(*) FROM reviews;"
```
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT app_name, COUNT(*) FROM reviews GROUP BY app_name;"
```

### **Step 10: Make Spark Helper Script Executable**
```bash
chmod +x scripts/helper_script.sh
```

### **Step 11: Fix Spark Ivy Cache Permissions**
```bash
docker exec -u root spark-master bash -c "mkdir -p /tmp/.ivy2/cache && chown -R spark:spark /tmp/.ivy2 && chmod -R 777 /tmp/.ivy2"
```

### **Step 12: Run Spark Batch Aggregates**
```bash
./scripts/helper_script.sh batch_aggregates.py
```

### **Step 13: Run Spark Dashboard Metrics**
```bash
./scripts/helper_script.sh dashboard_metric.py
```

### **Step 14: Verify All Dashboard Tables Have Data**
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT * FROM dashboard_overview;"
```
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT * FROM dashboard_rankings;"
```
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT * FROM dashboard_daily_stats LIMIT 5;"
```
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT * FROM dashboard_sentiment_dist;"
```
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT * FROM dashboard_rating_dist ORDER BY app_name, score;"
```
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT app_name, score, thumbsUpCount FROM dashboard_top_reviews LIMIT 5;"
```
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT * FROM dashboard_trending;"
```
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT * FROM dashboard_peak_hours WHERE app_name = 'chatgpt' ORDER BY hour;"
```

---

## 🌐 Access Web UIs

### **pgAdmin**
```
http://localhost:5050
Email: admin@admin.com
Password: admin
```

### **Spark Master UI**
```
http://localhost:8080
```

### **Airflow**
```
http://localhost:8082
```

---

## 🔄 Re-run Pipeline with Fresh Data
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "TRUNCATE TABLE reviews, daily_app_stats, dashboard_overview, dashboard_rankings, dashboard_daily_stats, dashboard_sentiment_dist, dashboard_rating_dist, dashboard_top_reviews, dashboard_trending, dashboard_peak_hours CASCADE;"
```
```bash
python producer/producer.py
```
```bash
python consumer/consumer.py
```
```bash
./scripts/helper_script.sh batch_aggregates.py
```
```bash
./scripts/helper_script.sh dashboard_metric.py
```

---

## 🛑 Stop All Services
```bash
docker-compose down
```

---

## 🔧 Troubleshooting Commands

### Restart Services
```bash
docker-compose down
```
```bash
docker-compose up -d
```
```bash
sleep 30
```

### Create Database Manually
```bash
docker exec -it postgres psql -U airflow -c "CREATE DATABASE llm_reviews;"
```
```bash
./scripts/setup_postgres.sh
```

### Fix Spark Ivy Permissions
```bash
docker exec -u root spark-master bash -c "mkdir -p /tmp/.ivy2/cache && chown -R spark:spark /tmp/.ivy2 && chmod -R 777 /tmp/.ivy2"
```

### View Service Logs
```bash
docker-compose logs -f kafka
```
```bash
docker-compose logs -f postgres
```
```bash
docker-compose logs -f spark-master
```
```bash
docker-compose logs -f airflow
```

---

## 🎯 Quick One-Liner (After First Setup)
```bash
python producer/producer.py && python consumer/consumer.py & sleep 15 && kill %1 && ./scripts/helper_script.sh batch_aggregates.py && ./scripts/helper_script.sh dashboard_metric.py
```

---

## ✅ Verification Commands

### Count reviews
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT COUNT(*) FROM reviews;"
```

### Check rankings
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT * FROM dashboard_rankings;"
```

### List all tables
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "\dt"
```

### Check table sizes
```bash
docker exec -it postgres psql -U airflow -d llm_reviews -c "SELECT schemaname, tablename, n_live_tup as row_count FROM pg_stat_user_tables ORDER BY n_live_tup DESC;"
```