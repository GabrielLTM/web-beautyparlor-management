"""
Módulo de segurança para o manuseamento de senhas.

Este ficheiro centraliza todas as operações criptográficas relacionadas com
as senhas dos utilizadores. Ele utiliza a biblioteca Passlib para implementar
o hashing de senhas de forma segura, garantindo que as senhas em texto puro
nunca sejam armazenadas no banco de dados.

A abordagem de hashing é fundamental para a segurança, pois é um processo de
mão única que não pode ser revertido, protegendo as credenciais dos utilizadores
mesmo em caso de uma violação de dados.
"""
from passlib.context import CryptContext

# Cria um contexto de criptografia, especificando o algoritmo de hash padrão.
# O 'bcrypt' é o padrão da indústria para hashing de senhas devido à sua
# lentidão computacional inerente, o que o torna resistente a ataques de força bruta.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se uma senha em texto puro corresponde a um hash armazenado.

    Args:
        senha_plana (str): A senha fornecida pelo utilizador no momento do login.
        senha_hash (str): O hash da senha que está armazenado no banco de dados.

    Returns:
        bool: True se a senha corresponder ao hash, False caso contrário.
    """
    return pwd_context.verify(senha_plana, senha_hash)


def gerar_hash_senha(senha: str) -> str:
    """
    Gera um hash seguro a partir de uma senha em texto puro.

    A função utiliza o contexto do Passlib, que automaticamente lida com a
    geração de um "salt" (sal) aleatório para cada senha, garantindo que
    senhas iguais resultem em hashes diferentes e seguros.

    Args:
        senha (str): A senha em texto puro a ser hasheada.

    Returns:
        str: O hash da senha, pronto para ser armazenado no banco de dados.
    """
    return pwd_context.hash(senha)
