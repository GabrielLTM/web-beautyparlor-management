from fastapi import Depends, HTTPException, Request
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# --- DEPENDÊNCIAS E SEGURANÇA ---
class NotAuthenticatedException(Exception):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(request: Request):
    user = request.session.get('user')
    if not user:
        raise NotAuthenticatedException
    return user

def get_current_admin_user(user: dict = Depends(get_current_user)):
    if user.get("funcao") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Esta área é restrita a administradores."
        )
    return user
