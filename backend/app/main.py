import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.journals import router as journals_router
from app.api.habits import router as habits_router
from app.api.habit_logs import router as habit_logs_router
from app.api.wellbeing_scores import router as wellbeing_scores_router
from app.api.insights import router as insights_router
from app.config import settings


logger = logging.getLogger("mindmirror")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="MindMirror API",
    description="AI-Based Personal Well-Being and Habit Intelligence System API",
    version="0.1.0",
)

# CORS configuration restricted to frontend local development origin
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catches unhandled exceptions and returns a generic 500 response without leaking internal details."""
    logger.error("Unhandled exception processing %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Include health router
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(journals_router)
app.include_router(habits_router)
app.include_router(habit_logs_router)
app.include_router(wellbeing_scores_router)
app.include_router(insights_router)