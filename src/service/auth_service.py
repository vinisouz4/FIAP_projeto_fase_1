from jose import JWTError, jwt
import time
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from src.log.logs import LoggerHandler
from src.core.configs import Settings

logger = LoggerHandler(__name__)
settings = Settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def authenticate_user(username: str, password: str):

    if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
        logger.INFO("User authenticated successfully.")
        return {"username": username, "password": password}
    else:
        logger.WARNING("Authentication failed for user.")
    return None

def create_access_token(username: str, expires_delta: int = 3600):
    expire = time.time() + expires_delta
    
    encoded = {
        "sub": username, 
        "exp": expire
    }

    logger.INFO(f"Access token created for user: {username} / Expires in: {expire}")

    return jwt.encode(encoded, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def current_user(token: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    
    logger.INFO(f"Current user: {username}")
    return username