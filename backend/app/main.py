import os
import secrets
from functools import lru_cache
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="JWT FastAPI Demo")


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 300
REFRESH_TOKEN_EXPIRE_SECONDS = 3600


class Settings(BaseModel):
    admin_username: str
    admin_password: str
    jwt_secret_key: str


@lru_cache
def get_settings() -> Settings:
    return Settings(
        admin_username=_require_env("APP_ADMIN_USERNAME"),
        admin_password=_require_env("APP_ADMIN_PASSWORD"),
        jwt_secret_key=_require_env("JWT_SECRET_KEY"),
    )


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


def _create_token(subject: str, token_type: str, expires_in_seconds: int) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=expires_in_seconds)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)


@app.on_event("startup")
def validate_settings() -> None:
    get_settings()


@app.post("/token")
def get_token(credentials: LoginRequest) -> dict:
    settings = get_settings()
    if not (
        secrets.compare_digest(credentials.username, settings.admin_username)
        and secrets.compare_digest(credentials.password, settings.admin_password)
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = _create_token(
        settings.admin_username, "access", ACCESS_TOKEN_EXPIRE_SECONDS
    )
    refresh_token = _create_token(
        settings.admin_username, "refresh", REFRESH_TOKEN_EXPIRE_SECONDS
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }


@app.post("/token/refresh")
def refresh_token(payload: RefreshRequest) -> dict:
    settings = get_settings()
    try:
        decoded = jwt.decode(
            payload.refresh_token,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub", "type"]},
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from exc

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token type")

    new_access_token = _create_token(decoded["sub"], "access", ACCESS_TOKEN_EXPIRE_SECONDS)
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }
