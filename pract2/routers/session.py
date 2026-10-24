from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone

from schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from core.security import verify_password, create_access_token, create_refresh_token, decode_token

from database.connection import get_db
from database.models import User, Tokens

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

import jwt


router = APIRouter(prefix="/session", tags=['Session'])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.scalar(select(User).where(User.username == data.username))

        if user is None or not verify_password(data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль", headers={"WWW-Authenticate": "Bearer"})

        access_token, access_expires_at = create_access_token(user.user_id, user.role_id)
        refresh_token, refresh_expires_at = create_refresh_token(user.user_id)

        token_record = Tokens(user_id=user.user_id, token=refresh_token, expires_at=refresh_expires_at)
        db.add(token_record)
        db.commit()

        return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_at=access_expires_at)
    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Всё, база данных была дропнута",)


@router.put('/refresh', response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(data.refresh_token, 'refresh')
        user_id = int(payload['sub'])
    except (jwt.InvalidTokenError, ValueError, TypeError, KeyError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен просрочен, купи новый', headers={"WWW-Authenticate": "Bearer"})

    try:
        token_record = db.scalar(select(Tokens).where(Tokens.token == data.refresh_token, Tokens.user_id == user_id))
        if token_record is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh-токен отозван или не найден", headers={"WWW-Authenticate": "Bearer"},)
        if token_record.expires_at <= datetime.now(timezone.utc):
            db.delete(token_record)
            db.commit()

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh-токен просрочен", headers={"WWW-Authenticate": "Bearer"},)
        user = db.get(User, user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Пользователь не найден",)

        access_token, access_expires_at = create_access_token(user.user_id, user.role_id)
        new_refresh_token, refresh_expires_at = create_refresh_token(user.user_id)

        token_record.token = new_refresh_token
        token_record.expires_at = refresh_expires_at
        db.commit()

        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token, expires_at=access_expires_at)
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении токенов",
        )