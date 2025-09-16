from fastapi import APIRouter, HTTPException
from typing import List

from src.service.auth_service import create_access_token, recreate_access_token
from src.models.auth_models import LoginRequest, TokenRefresh



router_auth = APIRouter(prefix="/auth")


@router_auth.post("/v1/login")
async def login(request: LoginRequest):
    """
    Authenticate a user and generate access and refresh tokens.
    Args:
        request (LoginRequest): The login request body containing username and password.
    Returns:
        dict: A dictionary containing the access and refresh tokens.
    """
    try:
        # Dummy authentication logic (replace with real authentication)
        if request.username == "admin" and request.password == "password":
            user_data = {"sub": request.username}
            
            access_token = create_access_token(data=user_data)

            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router_auth.post("/v1/refresh", response_model=TokenRefresh)
async def refresh_token(token: str):
    """
    Refresh the access token using a valid refresh token.
    Args:
        token (str): The refresh token.
    Returns:
        dict: A dictionary containing the new access token.
    """
    try:
        # Dummy logic to decode and validate the refresh token (replace with real validation)
        # Here we just assume the token is valid and contains the username
        user_data = {"sub": "admin"}  # Replace with actual data extracted from the token
        
        new_access_token = recreate_access_token(data=user_data)

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))