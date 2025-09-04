from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# ### A "MÁGICA" ACONTECE AQUI ###
# 1. Carrega todas as variáveis definidas no seu ficheiro .env
load_dotenv()

# 2. Busca a variável "DATABASE_URL" do ambiente, em vez de a ter escrita aqui.
# A sua senha agora está segura e fora do código.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# --- O RESTO DO FICHEIRO CONTINUA IGUAL ---
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

