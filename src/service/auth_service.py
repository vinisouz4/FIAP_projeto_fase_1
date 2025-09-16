from jose import JWTError, jwt
from typing import Dict
import time
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from src.log.logs import LoggerHandler
from src.core.configs import Settings

logger = LoggerHandler(__name__)
settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/v1/login")


def create_access_token(data: Dict, expires_delta: int = 900):
    try:
        to_encode = data.copy()
        
        expire = int(time.time()) + expires_delta

        to_encode.update(
            {
                "exp": expire, 
                "type": "access"
            }
        )

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        logger.INFO(f"Access token created successfully")
        
        return encoded_jwt
    except Exception as e:
        logger.ERROR(f"Error creating access token: {e}")
        raise e
    
def recreate_access_token(data: Dict, expires_delta: int = 3600):
    try:
        to_encode = data.copy()
        
        expire = int(time.time()) + expires_delta

        to_encode.update(
            {
                "exp": expire, 
                "type": "refresh"
            }
        )

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        logger.INFO(f"Refresh token created successfully")
        
        return encoded_jwt
    except Exception as e:
        logger.ERROR(f"Error creating refresh token: {e}")
        raise e
    
def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verifica se o token é válido e retorna o usuário.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )