"""
Define as dependências reutilizáveis para a injeção no FastAPI.

Este módulo centraliza a lógica para a gestão de sessões de banco de dados,
para a autenticação, e autorização de utilizadores. A utilização de dependências
permite que as nossas rotas permaneçam limpas e focadas na sua lógica de negócio,
delegando estas tarefas transversais para componentes reutilizáveis e testáveis.
"""
from fastapi import Depends, HTTPException, Request
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# --- DEPENDÊNCIAS E SEGURANÇA ---

class NotAuthenticatedException(Exception):
    """Exceção personalizada para ser levantada quando um utilizador não está autenticado."""
    pass

def get_db():
    """
    Dependência para a gestão de sessões do banco de dados.

    Este é um gerador (generator) que cria uma nova sessão do SQLAlchemy para cada
    requisição que a utiliza. O padrão 'try...yield...finally' garante que
    a sessão seja sempre fechada (`db.close()`) no final da requisição,
    mesmo que ocorra um erro, prevenindo o esgotamento de conexões com o banco.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    Dependência para obter o utilizador atualmente logado a partir da sessão.

    Esta função atua como um "porteiro" para as rotas. Ela verifica se existe
    uma sessão de utilizador ativa. Se não existir, levanta a exceção
    'NotAuthenticatedException', que é capturada pelo nosso handler global
    para redirecionar o utilizador para a página de login.

    Returns:
        dict: Os dados do utilizador armazenados na sessão.
    """
    user_id = request.session.get('user_id')
    if not user_id:
        raise NotAuthenticatedException
    user = db.query(models.Funcionario).filter(models.Funcionario.id == user_id).first()
    if not user or not user.is_ativo:
        raise NotAuthenticatedException
    return user

def get_current_admin_user(user: dict = Depends(get_current_user)):
    """
    Dependência que garante que o utilizador logado é um administrador.

    Esta função constrói sobre a dependência 'get_current_user'. Primeiro, ela
    garante que há um utilizador logado. Depois, ela verifica se a função ('funcao')
    desse utilizador é 'admin'. Se não for, ela levanta uma exceção HTTPException
    com o status 403 (Forbidden), negando o acesso à rota.

    Returns:
        dict: Os dados do utilizador, confirmados como sendo de um administrador.
    """
    if user.funcao != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Esta área é restrita a administradores."
        )
    return user

