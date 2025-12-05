from sqlalchemy import Column, String, Float, Integer, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Review(Base):
    __tablename__ = "reviews"

    # MUST MATCH EXACT DB COLUMN NAMES
    reviewid = Column("reviewId", String, primary_key=True)
    app_name = Column(String, nullable=False, index=True)
    score = Column(Float)
    content = Column(String)
    at = Column(DateTime, index=True)
    thumbsupcount = Column("thumbsUpCount", Integer)

    __table_args__ = (
        Index("idx_app_at", "app_name", "at"),
    )


class DailyAppStats(Base):
    __tablename__ = "daily_app_stats"

    # You defined PK as (app_name, day) in Postgres, but model didn’t match.
    # Better to reflect real DB: NO synthetic 'id'
    app_name = Column(String, primary_key=True)
    date = Column("day", DateTime, primary_key=True)
    total_reviews = Column("review_count", Integer)
    avg_rating = Column("avg_score", Float)
    avg_thumbs_up = Column(Float)

    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)


class DashboardSentimentDist(Base):
    __tablename__ = "dashboard_sentiment_dist"

    app_name = Column(String, primary_key=True)
    sentiment = Column(String, primary_key=True)
    count = Column(Integer)


class DashboardRatingDist(Base):
    __tablename__ = "dashboard_rating_dist"

    app_name = Column(String, primary_key=True)
    score = Column(Float, primary_key=True)
    count = Column(Integer)
