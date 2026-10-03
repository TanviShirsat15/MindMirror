from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.dependencies import get_current_user
from app.core.rate_limit import limiter
from app.core.security import create_access_token
from app.database import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserRead
from app.services.auth_service import authenticate_user, register_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
def register(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        return register_user(db, user_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(
    request: Request,
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        user_data.email,
        user_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        str(user.id),
        settings.JWT_EXPIRE_MINUTES,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/me", response_model=UserRead)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user