FROM bitnami/spark:latest

COPY sentiment_streaming_job.py /opt/bitnami/spark/app/sentiment_streaming_job.py
WORKDIR /opt/bitnami/spark

CMD ["spark-submit", "/opt/bitnami/spark/app/sentiment_streaming_job.py"]
