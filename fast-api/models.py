from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column, String, Float, Integer, DateTime, Date, BigInteger, Index
)

Base = declarative_base()

# -----------------------------------
#  REVIEWS TABLE (RAW DATA)
# -----------------------------------
class Review(Base):
    __tablename__ = "reviews"

    reviewid = Column(String, primary_key=True)
    app_name = Column(String, nullable=False, index=True)
    at = Column(DateTime, nullable=True, index=True)
    score = Column(Float, nullable=True)
    content = Column(String, nullable=True)
    thumbsupcount = Column(Integer, nullable=True)

    __table_args__ = (
           Index('idx_app_at', 'app_name', 'at'),
    )


# -----------------------------------
#  DAILY APP STATS (AGGREGATES BY SPARK)
# -----------------------------------
class DailyAppStats(Base):
    __tablename__ = "daily_app_stats"

    app_name = Column(String, primary_key=True)
    day = Column(Date, primary_key=True)

    review_count = Column(BigInteger)
    avg_score = Column(Float)
    avg_thumbs_up = Column(Float)


# -----------------------------------
#  DASHBOARD OVERVIEW
# -----------------------------------
class DashboardOverview(Base):
    __tablename__ = "dashboard_overview"

    metric_key = Column(String, primary_key=True)
    total_reviews = Column(BigInteger)
    total_apps = Column(BigInteger)
    overall_avg_rating = Column(Float)
    total_engagement = Column(BigInteger)
    updated_at = Column(DateTime)


# -----------------------------------
#  DASHBOARD RANKINGS
# -----------------------------------
class DashboardRankings(Base):
    __tablename__ = "dashboard_rankings"

    app_name = Column(String, primary_key=True)
    total_reviews = Column(BigInteger)
    avg_rating = Column(Float)
    avg_engagement = Column(Float)
    updated_at = Column(DateTime)


# -----------------------------------
#  DASHBOARD DAILY STATS
# -----------------------------------
class DashboardDailyStats(Base):
    __tablename__ = "dashboard_daily_stats"

    app_name = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)

    review_count = Column(BigInteger)
    avg_rating = Column(Float)
    avg_engagement = Column(Float)


# -----------------------------------
#  SENTIMENT DISTRIBUTION
# -----------------------------------
class DashboardSentimentDist(Base):
    __tablename__ = "dashboard_sentiment_dist"

    app_name = Column(String, primary_key=True)
    sentiment = Column(String, primary_key=True)
    count = Column(BigInteger)


# -----------------------------------
#  RATING DISTRIBUTION
# -----------------------------------
class DashboardRatingDist(Base):
    __tablename__ = "dashboard_rating_dist"

    app_name = Column(String, primary_key=True)
    score = Column(Float, primary_key=True)
    count = Column(BigInteger)


# -----------------------------------
#  TOP REVIEWS
# -----------------------------------
class DashboardTopReviews(Base):
    __tablename__ = "dashboard_top_reviews"

    reviewId = Column(String, primary_key=True)
    app_name = Column(String)
    content = Column(String)
    score = Column(Float)
    thumbsUpCount = Column(Integer)
    at = Column(DateTime)


# -----------------------------------
#  TRENDING APPS
# -----------------------------------
class DashboardTrending(Base):
    __tablename__ = "dashboard_trending"

    app_name = Column(String, primary_key=True)

    recent_rating = Column(Float)
    recent_reviews = Column(BigInteger)
    previous_rating = Column(Float)
    previous_reviews = Column(BigInteger)
    rating_change = Column(Float)
    review_growth = Column(BigInteger)
    updated_at = Column(DateTime)


# -----------------------------------
#  PEAK HOURS
# -----------------------------------
class DashboardPeakHours(Base):
    __tablename__ = "dashboard_peak_hours"

    app_name = Column(String, primary_key=True)
    hour = Column(Integer, primary_key=True)

    review_count = Column(BigInteger)
    avg_rating = Column(Float)
