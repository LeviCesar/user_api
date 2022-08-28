from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
from typing import Union
import jwt

from schemas.users import UserLogin, UserRegister
from schemas.default import Default
from schemas.auth import Token, RefreshToken, NewToken

from models.users import Users

from utils.token_auth import user_refresh_token
from config import (
    REFRESH_TOKEN_EXPIRE_DAYS,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY
)


router  = APIRouter()


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/sign-in", response_model=Token)
async def login_for_access_token(form_data: UserLogin):
    user = await Users.get_authenticated_user(username=form_data.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user deactivate'
        )
    
    validate = Users.verify_password(
        plain_password=form_data.password, hashed_password=user.hashed_password)
    
    if not validate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data  = {
        "sub": str(user.id),
        "token_type": "at+jwt"
    }
    access_token = create_access_token(
        data=access_token_data, expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_data = {
        "sub": str(user.id),
        "token_type": "rt+jwt"
    }
    refresh_token = create_access_token(
        data=refresh_token_data, expires_delta=refresh_token_expires, 
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post('/refresh-token', response_model=NewToken)
async def refresh_access_token(refresh_token: RefreshToken):
    user = await user_refresh_token(token=refresh_token.token)
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user deactivate'
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data  = {
        "sub": str(user.id),
        "token_type": "at+jwt"
    }
    access_token = create_access_token(
        data=access_token_data, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post('/register', status_code=201, response_model=Default)
async def register_user(new_user: UserRegister):
    detail, created = await Users.register_new_user(**new_user.dict())
    if not created:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=detail
        )
    return {
        'message': 'User Created'
    }