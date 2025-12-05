import os
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "llm_reviews")
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# ----------------------------------------
# Create async engine
# ----------------------------------------
engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    
    # asyncpg + SQLAlchemy 2.0 recommended:
    poolclass=NullPool,
    pool_pre_ping=True,
)

# ----------------------------------------
# Create async session factory
# ----------------------------------------
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# ----------------------------------------
# Dependency for FastAPI routes
# ----------------------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

