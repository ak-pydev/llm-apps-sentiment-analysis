from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}

dag = DAG(
    'cleanup_old_data',
    default_args=default_args,
    description='Clean up data older than 30 days',
    schedule_interval='0 3 * * 0',  # Run at 3 AM every Sunday
    catchup=False,
    tags=['cleanup', 'maintenance'],
)

cleanup_task = BashOperator(
    task_id='delete_old_reviews',
    bash_command='''
    docker exec postgres psql -U airflow -d llm_reviews -c "
    DELETE FROM reviews WHERE at < NOW() - INTERVAL '30 days';
    "
    ''',
    dag=dag,
)