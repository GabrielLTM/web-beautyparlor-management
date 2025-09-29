"""
Ponto de entrada principal e configuração da aplicação FastAPI.

Este módulo é o coração da aplicação. As suas responsabilidades são:

1.  Carregar as variáveis de ambiente de forma segura a partir do ficheiro .env.
2.  Garantir que todas as tabelas do banco de dados sejam criadas no arranque.
3.  Inicializar a instância principal da aplicação FastAPI.
4.  Configurar middlewares globais, como o de gestão de sessões.
5.  Definir handlers de exceção globais, como o de redirecionamento para login.
6.  Incluir e agregar todos os routers modulares (autenticacao, painel, admin) para construir a API completa.
"""
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
import models
from database import engine
import os
from dotenv import load_dotenv

from routers import autenticacao, painel, admin
from dependencies import NotAuthenticatedException

# Carrega as variáveis de ambiente definidas no ficheiro .env para o ambiente de execução.
load_dotenv()

# Garante que todas as tabelas definidas em models.py sejam criadas no banco de dados
# se ainda não existirem. Esta linha é executada uma vez, no arranque da aplicação.
models.Base.metadata.create_all(bind=engine)

# Cria a instância principal da aplicação FastAPI, com metadados para documentação.
app = FastAPI(
    title="API do Salão de Beleza",
    description="API para gerenciar agendamentos, funcionários e serviços."
)


@app.exception_handler(NotAuthenticatedException)
async def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """

    Handler de exceção global para utilizadores não autenticados.

    Este handler é acionado sempre que a exceção 'NotAuthenticatedException' é
    levantada em qualquer parte da aplicação (especificamente, na dependência
    'get_current_user'). A sua única responsabilidade é redirecionar o
    utilizador para a página de login, centralizando a lógica de proteção de
    rotas.
    """
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


# Adiciona o middleware de sessão à aplicação. Isto permite que a aplicação
# armazene dados (como a identidade do utilizador logado) entre requisições.
# A 'secret_key' é lida de forma segura a partir das variáveis de ambiente.
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# Inclui os routers modulares na aplicação principal.
# Esta é a base da nossa arquitetura organizada: cada router traz consigo
# o seu próprio conjunto de rotas, que são agregadas aqui.
app.include_router(autenticacao.router)
app.include_router(painel.router)
app.include_router(admin.router)

