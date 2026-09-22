import logging
from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def get_health() -> dict[str, str]:
    db_status = "connected"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        logger.error("Health check database error: %s", exc)
        db_status = "unreachable"

    return {
        "status": "ok",
        "db": db_status,
    }
