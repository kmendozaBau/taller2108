import os
import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from functools import lru_cache

import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, SecretStr


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
    admin_password: SecretStr
    jwt_secret_key: SecretStr


@lru_cache
def get_settings() -> Settings:
    return Settings(
        admin_username=_require_env("APP_ADMIN_USERNAME"),
        admin_password=SecretStr(_require_env("APP_ADMIN_PASSWORD")),
        jwt_secret_key=SecretStr(_require_env("JWT_SECRET_KEY")),
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
    return jwt.encode(
        payload, settings.jwt_secret_key.get_secret_value(), algorithm=ALGORITHM
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    get_settings()
    yield


app = FastAPI(title="JWT FastAPI Demo", lifespan=lifespan)


@app.post("/token")
def get_token(credentials: LoginRequest) -> dict:
    settings = get_settings()
    if not (
        secrets.compare_digest(credentials.username, settings.admin_username)
        and secrets.compare_digest(
            credentials.password, settings.admin_password.get_secret_value()
        )
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
            settings.jwt_secret_key.get_secret_value(),
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
