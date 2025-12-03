from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StringType

# Simple streaming job: read JSON messages from Kafka topic 'sentiment', compute sentiment
# NOTE: This example uses TextBlob for sentiment; in production include proper NLP model.

try:
    from textblob import TextBlob
except Exception:
    TextBlob = None


def sentiment(text):
    if not text:
        return 'neutral'
    if TextBlob:
        try:
            p = TextBlob(text).sentiment.polarity
            if p > 0:
                return 'positive'
            if p < 0:
                return 'negative'
            return 'neutral'
        except Exception:
            return 'neutral'
    # fallback heuristic
    lw = text.lower()
    if any(w in lw for w in ['love', 'great', 'excellent', 'awesome', 'amazing']):
        return 'positive'
    if any(w in lw for w in ['hate', 'terrible', 'bad', 'awful', 'worst']):
        return 'negative'
    return 'neutral'

udf_sentiment = udf(sentiment, StringType())

if __name__ == '__main__':
    spark = SparkSession.builder.appName('SentimentStreamingJob').getOrCreate()

    kafka_bootstrap = 'kafka:9092'

    schema = StructType().add('text', StringType())

    df = spark.readStream.format('kafka') \
        .option('kafka.bootstrap.servers', kafka_bootstrap) \
        .option('subscribe', 'sentiment') \
        .option('startingOffsets', 'earliest') \
        .load()

    json_df = df.selectExpr('CAST(value AS STRING) as value')
    parsed = json_df.select(from_json(col('value'), schema).alias('data')).select('data.*')
    with_sent = parsed.withColumn('sentiment', udf_sentiment(col('text')))

    # For demo purposes, write to console. In production write to Cassandra.
    query = with_sent.writeStream.format('console').outputMode('append').start()
    query.awaitTermination()
