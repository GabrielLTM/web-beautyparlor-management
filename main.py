from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette import status
from starlette.middleware.sessions import SessionMiddleware
import models
from database import engine
import os
from dotenv import load_dotenv

# Importa os nossos novos routers
from routers import autenticacao, painel, admin
from dependencies import NotAuthenticatedException

# ### A "MÁGICA" ACONTECE AQUI ###
# Carrega as variáveis de ambiente definidas no seu ficheiro .env
load_dotenv()

# Garante que as tabelas sejam criadas no arranque
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API do Salão de Beleza",
    description="API para gerenciar agendamentos, funcionários e serviços."
)

@app.exception_handler(NotAuthenticatedException)
async def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

# ### LINHA ALTERADA ###
# Agora lê a chave secreta de forma segura a partir da variável de ambiente.
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# Incluímos os routers na aplicação principal.
app.include_router(autenticacao.router)
app.include_router(painel.router)
app.include_router(admin.router)

