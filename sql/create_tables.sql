-- Create database
CREATE DATABASE llm_reviews;

-- Connect to database
\c llm_reviews

-- Main reviews table
CREATE TABLE IF NOT EXISTS reviews (
    app_name VARCHAR(255),
    reviewId VARCHAR(255) PRIMARY KEY,
    at TIMESTAMP,
    score DOUBLE PRECISION,
    content TEXT,
    thumbsUpCount INTEGER
);

-- Daily aggregates table
CREATE TABLE IF NOT EXISTS daily_app_stats (
    app_name VARCHAR(255),
    day DATE,
    review_count BIGINT,
    avg_score DOUBLE PRECISION,
    avg_thumbs_up DOUBLE PRECISION,
    PRIMARY KEY (app_name, day)
);

-- Dashboard tables
CREATE TABLE IF NOT EXISTS dashboard_overview (
    metric_key VARCHAR(50) PRIMARY KEY,
    total_reviews BIGINT,
    total_apps BIGINT,
    overall_avg_rating DOUBLE PRECISION,
    total_engagement BIGINT,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dashboard_rankings (
    app_name VARCHAR(255) PRIMARY KEY,
    total_reviews BIGINT,
    avg_rating DOUBLE PRECISION,
    avg_engagement DOUBLE PRECISION,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dashboard_daily_stats (
    app_name VARCHAR(255),
    date DATE,
    review_count BIGINT,
    avg_rating DOUBLE PRECISION,
    avg_engagement DOUBLE PRECISION,
    PRIMARY KEY (app_name, date)
);

CREATE TABLE IF NOT EXISTS dashboard_sentiment_dist (
    app_name VARCHAR(255),
    sentiment VARCHAR(50),
    count BIGINT,
    PRIMARY KEY (app_name, sentiment)
);

CREATE TABLE IF NOT EXISTS dashboard_rating_dist (
    app_name VARCHAR(255),
    score DOUBLE PRECISION,
    count BIGINT,
    PRIMARY KEY (app_name, score)
);

CREATE TABLE IF NOT EXISTS dashboard_top_reviews (
    reviewId VARCHAR(255) PRIMARY KEY,
    app_name VARCHAR(255),
    content TEXT,
    score DOUBLE PRECISION,
    thumbsUpCount INTEGER,
    at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dashboard_trending (
    app_name VARCHAR(255) PRIMARY KEY,
    recent_rating DOUBLE PRECISION,
    recent_reviews BIGINT,
    previous_rating DOUBLE PRECISION,
    previous_reviews BIGINT,
    rating_change DOUBLE PRECISION,
    review_growth BIGINT,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dashboard_peak_hours (
    app_name VARCHAR(255),
    hour INTEGER,
    review_count BIGINT,
    avg_rating DOUBLE PRECISION,
    PRIMARY KEY (app_name, hour)
);