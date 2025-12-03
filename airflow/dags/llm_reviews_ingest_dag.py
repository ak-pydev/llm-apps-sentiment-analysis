from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# This DAG queries Cassandra to produce a daily aggregate of sentiment counts.
# It assumes the Cassandra keyspace/table created in cassandra/init.cql.

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='sentiment_daily_stats',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['sentiment'],
) as dag:

    def query_cassandra(**context):
        try:
            from cassandra.cluster import Cluster
            cluster = Cluster(['cassandra'])
            session = cluster.connect('sentiment')
            rows = session.execute("SELECT sentiment, count(*) as cnt FROM messages GROUP BY sentiment")
            stats = {row.sentiment: row.cnt for row in rows}
            print('Daily sentiment stats:', stats)
        except Exception as e:
            print('Could not query Cassandra:', e)
            raise

    run_query = PythonOperator(
        task_id='query_cassandra',
        python_callable=query_cassandra,
        provide_context=True,
    )

    run_query
