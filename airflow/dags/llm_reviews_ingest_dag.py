from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'llm_reviews_pipeline',
    default_args=default_args,
    description='Complete LLM Reviews Data Pipeline',
    schedule_interval='@daily',  # Run once per day
    catchup=False,
    tags=['llm', 'reviews', 'spark'],
)

# Task 1: Check if services are healthy
check_services = BashOperator(
    task_id='check_services',
    bash_command='''
    docker exec postgres pg_isready -U airflow &&
    docker exec kafka kafka-broker-api-versions.sh --bootstrap-server localhost:9092 &&
    docker exec spark-master curl -f http://localhost:8080
    ''',
    dag=dag,
)

# Task 2: Run Producer (CSV → Kafka)
run_producer = BashOperator(
    task_id='run_producer',
    bash_command='cd /opt/airflow && python producer/producer.py',
    dag=dag,
)

# Task 3: Run Consumer (Kafka → PostgreSQL)
# Note: Run for 30 seconds then timeout
run_consumer = BashOperator(
    task_id='run_consumer',
    bash_command='cd /opt/airflow && timeout 30s python consumer/consumer.py || true',
    dag=dag,
)

# Task 4: Run Spark Batch Aggregates
run_batch_aggregates = BashOperator(
    task_id='run_batch_aggregates',
    bash_command='''
    docker exec spark-master /opt/spark/bin/spark-submit \
      --master spark://spark-master:7077 \
      --packages org.postgresql:postgresql:42.6.0 \
      --conf spark.jars.ivy=/tmp/.ivy2 \
      /opt/spark-jobs/batch_aggregates.py
    ''',
    dag=dag,
)

# Task 5: Run Spark Dashboard Metrics
run_dashboard_metrics = BashOperator(
    task_id='run_dashboard_metrics',
    bash_command='''
    docker exec spark-master /opt/spark/bin/spark-submit \
      --master spark://spark-master:7077 \
      --packages org.postgresql:postgresql:42.6.0 \
      --conf spark.jars.ivy=/tmp/.ivy2 \
      /opt/spark-jobs/dashboard_metric.py
    ''',
    dag=dag,
)

# Task 6: Verify Results
verify_results = BashOperator(
    task_id='verify_results',
    bash_command='''
    docker exec postgres psql -U airflow -d llm_reviews -c "
    SELECT 
        'reviews' as table_name, COUNT(*) as count FROM reviews
    UNION ALL
    SELECT 
        'dashboard_rankings', COUNT(*) FROM dashboard_rankings
    UNION ALL
    SELECT 
        'daily_app_stats', COUNT(*) FROM daily_app_stats;
    "
    ''',
    dag=dag,
)

# Define task dependencies (order of execution)
check_services >> run_producer >> run_consumer >> run_batch_aggregates >> run_dashboard_metrics >> verify_results