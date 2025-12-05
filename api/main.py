import os
from datetime import date, datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cassandra.cluster import Cluster

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "llm_reviews")


class DailyStat(BaseModel):
    app_name: str
    day: date
    review_count: int
    avg_score: float
    avg_thumbs_up: Optional[float]


class Review(BaseModel):
    app_name: str
    reviewId: str
    at: Optional[datetime]
    score: Optional[float]
    content: Optional[str]
    thumbsUpCount: Optional[int]


app = FastAPI(title="LLM App Reviews API")

cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
session = cluster.connect()
session.set_keyspace(KEYSPACE)


@app.get("/apps", response_model=List[str])
def list_apps():
    rows = session.execute("SELECT DISTINCT app_name FROM reviews_by_app;")
    apps = sorted([r.app_name for r in rows if r.app_name])
    return apps


@app.get("/apps/{app_name}/stats", response_model=List[DailyStat])
def app_stats(app_name: str, days: int = 30):
    rows = session.execute(
        """
        SELECT app_name, day, review_count, avg_score, avg_thumbs_up
        FROM daily_app_stats
        WHERE app_name = %s
        LIMIT 365
        """,
        (app_name,),
    )
    stats = [
        DailyStat(
            app_name=row.app_name,
            day=row.day,
            review_count=row.review_count,
            avg_score=row.avg_score,
            avg_thumbs_up=row.avg_thumbs_up,
        )
        for row in rows
    ]
    if not stats:
        raise HTTPException(status_code=404, detail="No stats for this app")
    stats = sorted(stats, key=lambda r: r.day, reverse=True)[:days]
    return stats


@app.get("/apps/{app_name}/reviews", response_model=List[Review])
def app_reviews(app_name: str, limit: int = 50):
    rows = session.execute(
        """
        SELECT app_name, reviewId, at, score, content, thumbsUpCount
        FROM reviews_by_app
        WHERE app_name = %s
        LIMIT %s
        """,
        (app_name, limit),
    )
    return [
        Review(
            app_name=row.app_name,
            reviewId=row.reviewid,
            at=row.at,
            score=row.score,
            content=row.content,
            thumbsUpCount=row.thumbsupcount,
        )
        for row in rows
    ]
