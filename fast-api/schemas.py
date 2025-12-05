from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# ───────────────────────────────────────────────
# MAIN REVIEWS (matches table: reviews)
# ───────────────────────────────────────────────

class ReviewResponse(BaseModel):
    reviewid: str
    app_name: str
    score: Optional[float] = None
    content: Optional[str] = None
    at: Optional[datetime] = None
    thumbsupcount: Optional[int] = None

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# APP STATS (aggregated per app)
# ───────────────────────────────────────────────

class AppStatsResponse(BaseModel):
    app_name: str
    total_reviews: int
    avg_rating: Optional[float]
    positive_count: int
    negative_count: int
    neutral_count: int
    positive_percentage: Optional[float]

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# DAILY APP STATS (for specific app)
# matches daily_app_stats table
# ───────────────────────────────────────────────

class DailyStatResponse(BaseModel):
    date: date
    total_reviews: int
    avg_rating: Optional[float]
    positive_count: int
    negative_count: int
    neutral_count: int

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# DASHBOARD OVERVIEW
# matches dashboard_overview table
# ───────────────────────────────────────────────

class DashboardOverviewResponse(BaseModel):
    total_reviews: int
    total_apps: int
    avg_rating: Optional[float]
    positive_percentage: Optional[float]
    updated_at: datetime

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# DASHBOARD RANKINGS
# matches dashboard_rankings table
# ───────────────────────────────────────────────

class AppRankingResponse(BaseModel):
    app_name: str
    total_reviews: int
    avg_rating: Optional[float]
    positive_percentage: Optional[float]
    rank_by_reviews: Optional[int]
    rank_by_rating: Optional[int]

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# SENTIMENT DISTRIBUTION
# matches dashboard_sentiment_dist table
# ───────────────────────────────────────────────

class SentimentDistResponse(BaseModel):
    app_name: str
    positive: int
    negative: int
    neutral: int

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# RATING DISTRIBUTION
# matches dashboard_rating_dist table
# ───────────────────────────────────────────────

class RatingDistResponse(BaseModel):
    app_name: str
    rating_1: int
    rating_2: int
    rating_3: int
    rating_4: int
    rating_5: int

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# TOP REVIEWS
# matches dashboard_top_reviews table
# ───────────────────────────────────────────────

class TopReviewResponse(BaseModel):
    app_name: str
    review_id: str
    score: Optional[float]
    content: Optional[str]
    thumbsupcount: Optional[int]
    at: datetime

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# TRENDING APPS
# matches dashboard_trending table
# ───────────────────────────────────────────────

class TrendingResponse(BaseModel):
    app_name: str
    recent_rating: Optional[float]
    recent_reviews: int
    previous_rating: Optional[float]
    previous_reviews: int
    rating_change: Optional[float]
    review_growth: Optional[int]
    updated_at: datetime

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# PEAK HOURS
# matches dashboard_peak_hours table
# ───────────────────────────────────────────────

class PeakHourResponse(BaseModel):
    app_name: str
    hour: int
    review_count: int
    avg_rating: Optional[float]

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# COMPOSITE RESPONSES (used by /apps/{app_name})
# ───────────────────────────────────────────────

class AppDetailResponse(BaseModel):
    app_name: str
    stats: AppStatsResponse
    daily_stats: List[DailyStatResponse]
    sentiment_dist: SentimentDistResponse
    rating_dist: RatingDistResponse

    class Config:
        from_attributes = True


# ───────────────────────────────────────────────
# FULL DASHBOARD RESPONSE
# ───────────────────────────────────────────────

class DashboardFullResponse(BaseModel):
    overview: DashboardOverviewResponse
    rankings: List[AppRankingResponse]
    daily_stats: List[DailyStatResponse]
    trending: List[TrendingResponse]
    peak_hours: List[PeakHourResponse]

    class Config:
        from_attributes = True
