from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from db import get_db
from models import (
    Review,
    DailyAppStats,
    DashboardOverview,
    DashboardRankings,
    DashboardDailyStats,
    DashboardSentimentDist,
    DashboardRatingDist,
    DashboardTrending,
    DashboardPeakHours,
)
from schemas import (
    ReviewResponse,
    DailyStatResponse,
    SentimentDistResponse,
    RatingDistResponse,
    DashboardOverviewResponse,
    AppRankingResponse,
    TrendingResponse,
    PeakHourResponse,
    AppDetailResponse,
    DashboardFullResponse,
)

app = FastAPI(title="LLM App Analytics API", version="1.0")


# -------------------------------------------------------
# LIST ALL APPS
# -------------------------------------------------------
@app.get("/apps", response_model=list[str])
async def list_apps(db: AsyncSession = Depends(get_db)):
    stmt = select(Review.app_name).distinct().order_by(Review.app_name)
    rows = await db.execute(stmt)
    apps = rows.scalars().all()
    return apps


# -------------------------------------------------------
# APP REVIEWS
# -------------------------------------------------------
@app.get("/apps/{app_name}/reviews", response_model=list[ReviewResponse])
async def app_reviews(app_name: str, limit: int = 50, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Review)
        .where(Review.app_name == app_name)
        .order_by(desc(Review.at))
        .limit(limit)
    )
    result = await db.execute(stmt)
    reviews = result.scalars().all()
    return reviews


# -------------------------------------------------------
# APP DETAIL (daily stats + sentiment + rating dist)
# -------------------------------------------------------
@app.get("/apps/{app_name}/detail", response_model=AppDetailResponse)
async def app_detail(app_name: str, db: AsyncSession = Depends(get_db)):

    daily_stmt = select(DailyAppStats).where(DailyAppStats.app_name == app_name)
    sentiment_stmt = select(DashboardSentimentDist).where(DashboardSentimentDist.app_name == app_name)
    rating_stmt = select(DashboardRatingDist).where(DashboardRatingDist.app_name == app_name)

    daily_rows = (await db.execute(daily_stmt)).scalars().all()
    sentiment_row = (await db.execute(sentiment_stmt)).scalar_one_or_none()
    rating_row = (await db.execute(rating_stmt)).scalar_one_or_none()

    if not daily_rows:
        raise HTTPException(404, "App not found")

    return AppDetailResponse(
        app_name=app_name,
        daily_stats=daily_rows,
        sentiment_dist=sentiment_row,
        rating_dist=rating_row,
    )


# -------------------------------------------------------
# FULL DASHBOARD SUMMARY
# -------------------------------------------------------
@app.get("/dashboard", response_model=DashboardFullResponse)
async def dashboard(db: AsyncSession = Depends(get_db)):

    overview = (await db.execute(
        select(DashboardOverview).order_by(desc(DashboardOverview.updated_at)).limit(1)
    )).scalar_one_or_none()

    rankings = (await db.execute(
        select(DashboardRankings).order_by(desc(DashboardRankings.total_reviews))
    )).scalars().all()

    daily = (await db.execute(
        select(DashboardDailyStats).order_by(desc(DashboardDailyStats.date))
    )).scalars().all()

    trending = (await db.execute(
        select(DashboardTrending).order_by(desc(DashboardTrending.trend_score))
    )).scalars().all()

    peak_hours = (await db.execute(
        select(DashboardPeakHours).order_by(DashboardPeakHours.hour)
    )).scalars().all()

    return DashboardFullResponse(
        overview=overview,
        rankings=rankings,
        daily_stats=daily,
        trending=trending,
        peak_hours=peak_hours
    )
