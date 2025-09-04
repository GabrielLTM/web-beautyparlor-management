from passlib.context import CryptContext

# Cria um contexto, especificando o algoritmo de hash padrão (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se uma senha plana corresponde a um hash."""
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    """Gera o hash de uma senha."""
    return pwd_context.hash(senha)