from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi.templating import Jinja2Templates

import models
from security import verificar_senha
from dependencies import get_db

router = APIRouter()

# Configuração dos Templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@router.get("/login", response_class=HTMLResponse, tags=["Autenticação"])
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", tags=["Autenticação"])
async def process_login(request: Request, db: Session = Depends(get_db), username: str = Form(...),
                        password: str = Form(...)):
    funcionario = db.query(models.Funcionario).filter(models.Funcionario.nome == username).first()
    if not funcionario or not verificar_senha(password, funcionario.senha_hash):
        return templates.TemplateResponse("login.html",
                                          {"request": request, "error": "Nome de usuário ou senha incorretos."})
    if not funcionario.is_ativo:
        return templates.TemplateResponse("login.html",
                                          {"request": request, "error": "Este usuário está inativo. Contate o administrador."})
    request.session['user'] = {"id": funcionario.id, "nome": funcionario.nome, "cargo": funcionario.cargo,
                               "funcao": funcionario.funcao}
    return RedirectResponse(url="/painel", status_code=status.HTTP_303_SEE_OTHER)
