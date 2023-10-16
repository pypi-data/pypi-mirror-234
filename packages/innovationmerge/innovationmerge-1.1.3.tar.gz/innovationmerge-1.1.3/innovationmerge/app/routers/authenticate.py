from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

# Custom imports
from innovationmerge.app.schemas.user_schema import Token, User
from innovationmerge.app.security import (
    authenticate_user,
    fake_users_db,
    create_access_token,
    get_current_active_user,
)
from innovationmerge.config import configs

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = configs.ACCESS_TOKEN_EXPIRE_MINUTES


@router.post("/authenticate", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
