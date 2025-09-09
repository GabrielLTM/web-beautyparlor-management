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
    """
    Exibe a página de login para o usuário.

    Esta é uma rota GET simples que apenas renderiza e retorna o template HTML do formulário de login.

    Args:
        request (Request): O objeto de requisição do FastAPI, necessário para a renderização do template.

    Returns:
        TemplateResponse: Uma resposta HTML que renderiza a página 'login.html'.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", tags=["Autenticação"])
async def process_login(request: Request, db: Session = Depends(get_db), username: str = Form(...),
                        password: str = Form(...)):
    """
    Processa os dados do formulário de login e autentica o usuário.

    Esta rota POST recebe o nome de usuário e a senha enviados pelo formulário.
    Ela executa uma série de verificações de segurança:
    1. Busca o funcionário pelo nome de usuário no banco de dados.
    2. Compara a senha fornecida com o hash seguro armazenado.
    3. Verifica se a conta do funcionário está ativa.

    Se a autenticação for bem-sucedida, cria uma sessão para o usuário
    e o redireciona para o painel principal. Caso contrário, retorna
    a página de login com uma mensagem de erro apropriada.

    Args:
        request (Request): O objeto de requisição do FastAPI, usado para gerenciar a sessão.
        db (Session): A sessão do banco de dados, injetada como dependência.
        username (str): O nome de usuário recebido do formulário de login.
        password (str): A senha recebida do formulário de login.

    Returns:
        RedirectResponse: Em caso de sucesso, redireciona o usuário para a rota '/painel'.
        TemplateResponse: Em caso de falha, re-renderiza a página 'login.html' com uma mensagem de erro.
    """
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


@router.get("/logout", tags=["Autenticação"])
async def logout(request: Request):
    """
    Encerra a sessão do usuário (logout).

    Esta rota limpa os dados da sessão do usuário, efetivamente desconectando-o
    do sistema. Após limpar a sessão, o usuário é redirecionado para a
    página de login.

    Args:
        request (Request): O objeto de requisição do FastAPI, usado para acessar e limpar a sessão.

    Returns:
        RedirectResponse: Redireciona o usuário para a página de login ('/login').
    """
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
