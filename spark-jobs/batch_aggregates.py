# batch_aggregates.py
import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "llm_reviews")
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")

JDBC_URL = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def create_spark_connection():
    """Create Spark session with PostgreSQL JDBC driver"""
    try:
        spark = (
            SparkSession.builder
            .appName("LLMReviewsBatchAggregates")
            .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0")
            .getOrCreate()
        )
        
        spark.sparkContext.setLogLevel("ERROR")
        logger.info("Spark connection created successfully!")
        return spark
        
    except Exception as e:
        logger.error(f"Couldn't create the spark session due to exception {e}")
        return None


def read_from_postgres(spark):
    """Read data from PostgreSQL"""
    try:
        df = (
            spark.read
            .format("jdbc")
            .option("url", JDBC_URL)
            .option("dbtable", "reviews")
            .option("user", POSTGRES_USER)
            .option("password", POSTGRES_PASSWORD)
            .option("driver", "org.postgresql.Driver")
            .load()
        )
        logger.info(f"Successfully read from PostgreSQL table reviews")
        return df
        
    except Exception as e:
        logger.error(f"Failed to read from PostgreSQL: {e}")
        return None


def aggregate_data(df):
    """Perform aggregations on the data"""
    try:
        # Filter out null scores
        df = df.filter(F.col("score").isNotNull())
        
        # Aggregate by app and day
        agg = (
            df.withColumn("day", F.to_date(F.col("at")))
            .groupBy("app_name", "day")
            .agg(
                F.count("*").alias("review_count"),
                F.avg("score").alias("avg_score"),
                F.avg("thumbsUpCount").alias("avg_thumbs_up"),
            )
        )
        
        logger.info("Data aggregated successfully!")
        return agg
        
    except Exception as e:
        logger.error(f"Failed to aggregate data: {e}")
        return None


def write_to_postgres(df):
    """Write aggregated data back to PostgreSQL"""
    try:
        (
            df.write
            .format("jdbc")
            .option("url", JDBC_URL)
            .option("dbtable", "daily_app_stats")
            .option("user", POSTGRES_USER)
            .option("password", POSTGRES_PASSWORD)
            .option("driver", "org.postgresql.Driver")
            .mode("overwrite")  # or "append"
            .save()
        )
        logger.info(f"Successfully wrote to PostgreSQL table daily_app_stats")
        
    except Exception as e:
        logger.error(f"Failed to write to PostgreSQL: {e}")


def main():
    logger.info("Starting batch aggregates job...")
    logger.info(f"Using PostgreSQL host={POSTGRES_HOST}, database={POSTGRES_DB}")
    
    # Create Spark connection
    spark = create_spark_connection()
    
    if spark is not None:
        # Read from PostgreSQL
        df = read_from_postgres(spark)
        
        if df is not None:
            # Aggregate data
            agg_df = aggregate_data(df)
            
            if agg_df is not None:
                # Write back to PostgreSQL
                write_to_postgres(agg_df)
        
        # Stop Spark session
        spark.stop()
        logger.info("Batch job completed!")
    else:
        logger.error("Failed to create Spark connection. Exiting.")


if __name__ == "__main__":
    main()