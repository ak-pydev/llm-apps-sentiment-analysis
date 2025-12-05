# dashboard_metric.py
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
            .appName("DashboardMetrics")
            .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0")
            .getOrCreate()
        )
        
        spark.sparkContext.setLogLevel("ERROR")
        logger.info("Spark connection created successfully!")
        return spark
        
    except Exception as e:
        logger.error(f"Couldn't create the spark session due to exception {e}")
        return None


def main():
    logger.info("=" * 60)
    logger.info("Starting Dashboard Metrics Job")
    logger.info("=" * 60)
    logger.info(f"PostgreSQL Host: {POSTGRES_HOST}")
    logger.info(f"Database: {POSTGRES_DB}")
    logger.info("=" * 60)
    
    # Create Spark connection
    spark = create_spark_connection()
    
    if spark is None:
        logger.error("Failed to create Spark connection. Exiting.")
        return
    
    # Read reviews from PostgreSQL
    logger.info("\nReading reviews from PostgreSQL...")
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
    
    # Filter out null scores
    df = df.filter(F.col("score").isNotNull())
    
    review_count = df.count()
    logger.info(f"Loaded {review_count} reviews")
    
    if review_count == 0:
        logger.error("No reviews found!")
        spark.stop()
        return
    
    # 1. OVERVIEW METRICS
    logger.info("\n[1/8] Calculating overview metrics...")
    overview = df.agg(
        F.count("*").alias("total_reviews"),
        F.countDistinct("app_name").alias("total_apps"),
        F.avg("score").alias("overall_avg_rating"),
        F.sum("thumbsUpCount").alias("total_engagement")
    ).withColumn("metric_key", F.lit("summary")) \
     .withColumn("updated_at", F.current_timestamp())
    
    overview.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "dashboard_overview") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    
    logger.info("✓ Overview metrics saved")
    
    # 2. APP RANKINGS
    logger.info("\n[2/8] Calculating app rankings...")
    rankings = df.groupBy("app_name").agg(
        F.count("*").alias("total_reviews"),
        F.avg("score").alias("avg_rating"),
        F.avg("thumbsUpCount").alias("avg_engagement")
    ).withColumn("updated_at", F.current_timestamp()) \
      .orderBy(F.desc("avg_rating"))
    
    rankings.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "dashboard_rankings") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    
    logger.info("✓ App rankings saved")
    
    # 3. TIME SERIES (Daily)
    logger.info("\n[3/8] Calculating daily time series...")
    daily = (
        df.withColumn("date", F.to_date("at"))
        .groupBy("app_name", "date")
        .agg(
            F.count("*").alias("review_count"),
            F.avg("score").alias("avg_rating"),
            F.avg("thumbsUpCount").alias("avg_engagement")
        )
        .orderBy("date")
    )
    
    daily.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "dashboard_daily_stats") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    
    logger.info("✓ Daily time series saved")
    
    # 4. SENTIMENT DISTRIBUTION
    logger.info("\n[4/8] Calculating sentiment distribution...")
    df_with_sentiment = df.withColumn(
        "sentiment",
        F.when(F.col("score") >= 4.0, "positive")
        .when(F.col("score") <= 2.0, "negative")
        .otherwise("neutral")
    )
    
    sentiment_dist = df_with_sentiment.groupBy("app_name", "sentiment").agg(
        F.count("*").alias("count")
    )
    
    sentiment_dist.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "dashboard_sentiment_dist") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    
    logger.info("✓ Sentiment distribution saved")
    
    # 5. RATING DISTRIBUTION
    logger.info("\n[5/8] Calculating rating distribution...")
    rating_dist = df.groupBy("app_name", "score").agg(
        F.count("*").alias("count")
    ).orderBy("app_name", F.desc("score"))
    
    rating_dist.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "dashboard_rating_dist") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    
    logger.info("✓ Rating distribution saved")
    
    # 6. TOP REVIEWS
    logger.info("\n[6/8] Finding top reviews...")
    top_reviews = (
        df.select("app_name", "reviewId", "content", "score", "thumbsUpCount", "at")
        .orderBy(F.desc("thumbsUpCount"))
        .limit(100)
    )
    
    top_reviews.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "dashboard_top_reviews") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    
    logger.info("✓ Top reviews saved")
    
    # 7. TRENDING APPS
    logger.info("\n[7/8] Calculating trending apps...")
    
    recent_date = F.date_sub(F.current_date(), 7)
    previous_date = F.date_sub(F.current_date(), 14)
    
    recent = df.filter(F.col("at") >= recent_date).groupBy("app_name").agg(
        F.avg("score").alias("recent_rating"),
        F.count("*").alias("recent_reviews")
    )
    
    previous = df.filter(
        (F.col("at") >= previous_date) & (F.col("at") < recent_date)
    ).groupBy("app_name").agg(
        F.avg("score").alias("previous_rating"),
        F.count("*").alias("previous_reviews")
    )
    
    trends = recent.join(previous, "app_name", "outer").fillna(0)
    
    trends = trends.withColumn(
        "rating_change",
        F.col("recent_rating") - F.col("previous_rating")
    ).withColumn(
        "review_growth",
        F.col("recent_reviews") - F.col("previous_reviews")
    ).withColumn("updated_at", F.current_timestamp())
    
    trends.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "dashboard_trending") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    
    logger.info("✓ Trending data saved")
    
    # 8. PEAK HOURS
    logger.info("\n[8/8] Calculating peak hours...")
    
    peak_hours = (
        df.withColumn("hour", F.hour("at"))
        .groupBy("app_name", "hour")
        .agg(
            F.count("*").alias("review_count"),
            F.avg("score").alias("avg_rating")
        )
        .orderBy("app_name", "hour")
    )
    
    peak_hours.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "dashboard_peak_hours") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
    
    logger.info("✓ Peak hours saved")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Dashboard Metrics Job Completed Successfully!")
    logger.info("=" * 60)
    logger.info("\nGenerated metrics:")
    logger.info("  ✓ Overview metrics")
    logger.info("  ✓ App rankings")
    logger.info("  ✓ Daily time series")
    logger.info("  ✓ Sentiment distribution")
    logger.info("  ✓ Rating distribution")
    logger.info("  ✓ Top 100 reviews")
    logger.info("  ✓ Trending analysis")
    logger.info("  ✓ Peak hours")
    logger.info("\nAll data saved to PostgreSQL!")
    logger.info("=" * 60 + "\n")
    
    spark.stop()


if __name__ == "__main__":
    main()