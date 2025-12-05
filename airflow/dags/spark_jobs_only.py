from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'spark_jobs_only',
    default_args=default_args,
    description='Run only Spark batch jobs',
    schedule_interval='0 2 * * *',  # Run at 2 AM daily
    catchup=False,
    tags=['spark', 'batch'],
)

# Task 1: Batch Aggregates
batch_aggregates = BashOperator(
    task_id='batch_aggregates',
    bash_command='''
    docker exec spark-master /opt/spark/bin/spark-submit \
      --master spark://spark-master:7077 \
      --packages org.postgresql:postgresql:42.6.0 \
      --conf spark.jars.ivy=/tmp/.ivy2 \
      /opt/spark-jobs/batch_aggregates.py
    ''',
    dag=dag,
)

# Task 2: Dashboard Metrics
dashboard_metrics = BashOperator(
    task_id='dashboard_metrics',
    bash_command='''
    docker exec spark-master /opt/spark/bin/spark-submit \
      --master spark://spark-master:7077 \
      --packages org.postgresql:postgresql:42.6.0 \
      --conf spark.jars.ivy=/tmp/.ivy2 \
      /opt/spark-jobs/dashboard_metric.py
    ''',
    dag=dag,
)

batch_aggregates >> dashboard_metrics