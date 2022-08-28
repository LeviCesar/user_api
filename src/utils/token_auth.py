from fastapi import (
    HTTPException, 
    Header,
    status
)
import jwt

from models.users import Users

from config import (
    ALGORITHM,
    SECRET_KEY
)


async def user_auth_token( 
    token_bearer: str = Header(alias='Authorization')
) -> Users: 
    """Get current user from JWT token bearer infos.

    Args:
        token_bearer (str, optional): Defaults to Header(alias='Authorization').

    Raises:
        ResponseError: object

    Returns:
        Users: object
    """
    token_type, token = token_bearer.split(" ")
    if token_type != "Bearer":
        raise HTTPException(
            status_code=409, 
            detail="incorrect token type"
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        token_type = payload.get('token_type')
        if id is None or token_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='user not found'
            )
        
        if token_type != 'at+jwt':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect token"
            )
        
        return await Users.get_user(id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='token expired'
        )
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail='incorrect token'
        )

async def user_refresh_token(
    token: str
) -> Users:
    """Refresh token

    Args:
        token (str): refresh token to generate new token

    Raises:
        HTTPException: user not found
        HTTPException: expired refresh token necessary make login again
        HTTPException: incorrect token

    Returns:
        Users: Users object
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='user not found'
            )
        
        return await Users.get_user(id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='expired session'
        )
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail='incorrect token'
        )