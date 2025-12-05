from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from db import get_db
from models import (
    DashboardOverview,
    DashboardRankings,
    DashboardDailyStats,
    DashboardSentimentDist,
    DashboardRatingDist,
    DashboardTopReviews,
    DashboardTrending,
    DashboardPeakHours,
)

from schemas import (
    DashboardOverviewResponse,
    AppRankingResponse,
    DailyStatResponse,
    SentimentDistResponse,
    RatingDistResponse,
    TopReviewResponse,
    TrendingResponse,
    PeakHourResponse,
    DashboardFullResponse,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# =====================================================================
# OVERVIEW
# =====================================================================
@router.get("/overview", response_model=DashboardOverviewResponse)
async def get_dashboard_overview(db: AsyncSession = Depends(get_db)):

    stmt = (
        select(DashboardOverview)
        .order_by(DashboardOverview.updated_at.desc())
        .limit(1)
    )

    result = await db.execute(stmt)
    row = result.scalar_one_or_none()

    if not row:
        # fallback shape
        from datetime import datetime
        return DashboardOverviewResponse(
            total_reviews=0,
            total_apps=0,
            avg_rating=None,
            positive_percentage=None,
            updated_at=datetime.utcnow(),
        )

    return DashboardOverviewResponse(
        total_reviews=row.total_reviews,
        total_apps=row.total_apps,
        avg_rating=row.avg_rating,
        positive_percentage=row.positive_percentage,
        updated_at=row.updated_at,
    )


# =====================================================================
# APP RANKINGS
# =====================================================================
@router.get("/rankings", response_model=List[AppRankingResponse])
async def get_app_rankings(
    sort_by: str = Query(default="reviews", pattern="^(reviews|rating|sentiment)$"),
    limit: int = Query(default=10, le=100),
    db: AsyncSession = Depends(get_db),
):

    if sort_by == "reviews":
        stmt = select(DashboardRankings).order_by(desc(DashboardRankings.total_reviews)).limit(limit)
    elif sort_by == "rating":
        stmt = select(DashboardRankings).order_by(desc(DashboardRankings.avg_rating)).limit(limit)
    else:  # sentiment
        stmt = select(DashboardRankings).order_by(desc(DashboardRankings.positive_percentage)).limit(limit)

    result = await db.execute(stmt)
    rows = result.scalars().all()

    return [
        AppRankingResponse(
            app_name=r.app_name,
            total_reviews=r.total_reviews,
            avg_rating=r.avg_rating,
            positive_percentage=r.positive_percentage,
            rank_by_reviews=r.rank_by_reviews,
            rank_by_rating=r.rank_by_rating,
        )
        for r in rows
    ]


# =====================================================================
# GLOBAL DAILY STATS
# =====================================================================
@router.get("/daily-stats", response_model=List[DailyStatResponse])
async def get_dashboard_daily_stats(
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)

    stmt = (
        select(DashboardDailyStats)
        .where(DashboardDailyStats.date >= cutoff)
        .order_by(DashboardDailyStats.date.asc())
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()

    return [
        DailyStatResponse(
            date=r.date,
            total_reviews=r.new_reviews,
            avg_rating=r.avg_rating,
            positive_count=r.positive_count,
            negative_count=r.negative_count,
            neutral_count=r.neutral_count,
        )
        for r in rows
    ]


# =====================================================================
# SENTIMENT DISTRIBUTION
# =====================================================================
@router.get("/sentiment-distribution", response_model=List[SentimentDistResponse])
async def get_sentiment_distribution(
    limit: int = Query(default=10, le=100),
    db: AsyncSession = Depends(get_db),
):

    stmt = select(DashboardSentimentDist).limit(limit)
    result = await db.execute(stmt)
    rows = result.scalars().all()

    return [
        SentimentDistResponse(
            app_name=r.app_name,
            positive=r.positive,
            negative=r.negative,
            neutral=r.neutral,
        )
        for r in rows
    ]


# =====================================================================
# RATING DISTRIBUTION
# =====================================================================
@router.get("/rating-distribution", response_model=List[RatingDistResponse])
async def get_rating_distribution(
    limit: int = Query(default=10, le=100),
    db: AsyncSession = Depends(get_db),
):

    stmt = select(DashboardRatingDist).limit(limit)
    result = await db.execute(stmt)
    rows = result.scalars().all()

    return [
        RatingDistResponse(
            app_name=r.app_name,
            rating_1=r.rating_1,
            rating_2=r.rating_2,
            rating_3=r.rating_3,
            rating_4=r.rating_4,
            rating_5=r.rating_5,
        )
        for r in rows
    ]


# =====================================================================
# TOP REVIEWS
# =====================================================================
@router.get("/top-reviews", response_model=List[TopReviewResponse])
async def get_top_reviews(
    sentiment: str = Query(default="positive", pattern="^(positive|negative)$"),
    limit: int = Query(default=20, le=100),
    db: AsyncSession = Depends(get_db),
):
    is_top = 1 if sentiment == "positive" else -1

    stmt = (
        select(DashboardTopReviews)
        .where(DashboardTopReviews.is_top == is_top)
        .order_by(DashboardTopReviews.created_at.desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()

    return [
        TopReviewResponse(
            app_name=r.app_name,
            review_id=r.review_id,
            rating=r.rating,
            sentiment=sentiment,
            text=r.text,
            is_top=r.is_top,
            created_at=r.created_at,
        )
        for r in rows
    ]


# =====================================================================
# TRENDING APPS
# =====================================================================
@router.get("/trending", response_model=List[TrendingResponse])
async def get_trending_apps(
    limit: int = Query(default=10, le=50),
    db: AsyncSession = Depends(get_db),
):

    stmt = select(DashboardTrending).order_by(desc(DashboardTrending.trend_score)).limit(limit)
    result = await db.execute(stmt)
    rows = result.scalars().all()

    return [
        TrendingResponse(
            app_name=r.app_name,
            trend_score=r.trend_score,
            recent_reviews=r.recent_reviews,
            growth=r.growth,
        )
        for r in rows
    ]


# =====================================================================
# PEAK HOURS
# =====================================================================
@router.get("/peak-hours", response_model=List[PeakHourResponse])
async def get_peak_hours(db: AsyncSession = Depends(get_db)):

    stmt = select(DashboardPeakHours).order_by(DashboardPeakHours.hour.asc())
    result = await db.execute(stmt)
    rows = result.scalars().all()

    return [
        PeakHourResponse(
            hour=r.hour,
            review_count=r.review_count,
            avg_rating=r.avg_rating,
        )
        for r in rows
    ]


# =====================================================================
# FULL DASHBOARD RESPONSE
# =====================================================================
@router.get("/full", response_model=DashboardFullResponse)
async def get_full_dashboard(db: AsyncSession = Depends(get_db)):

    overview = await get_dashboard_overview(db)
    rankings = await get_app_rankings(limit=5, db=db)
    daily_stats = await get_dashboard_daily_stats(days=30, db=db)
    trending = await get_trending_apps(limit=5, db=db)
    peak_hours = await get_peak_hours(db)

    return DashboardFullResponse(
        overview=overview,
        rankings=rankings,
        daily_stats=daily_stats,
        trending=trending,
        peak_hours=peak_hours,
    )
