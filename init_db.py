"""
Script de utilidade para inicializar o banco de dados.

ATENÇÃO: Este é um script destrutivo e deve ser usado apenas em ambiente
de desenvolvimento. Ele não faz parte da aplicação principal.

O seu propósito é recriar completamente a estrutura do banco de dados e,
opcionalmente, popular as tabelas com dados iniciais ("seeding") para facilitar os testes e o desenvolvimento.

O script executa as seguintes ações:
1.  Destrói todas as tabelas existentes no banco de dados (`drop_all`).
2.  Cria todas as tabelas novamente com base na estrutura definida em `models.py` (`create_all`).
3.  Verifica se a tabela de funcionários está vazia. Se estiver, ele insere um conjunto de dados iniciais
(funcionários e serviços) para que a aplicação possa ser usada imediatamente.
"""
from decimal import Decimal
from database import engine, Base, SessionLocal
import models
from security import gerar_hash_senha

# --- DESTRUINDO E CRIANDO AS TABELAS ---

print("Iniciando a recriação das tabelas no banco de dados...")
# Apaga todas as tabelas existentes. Perigoso em produção!
Base.metadata.drop_all(bind=engine)
print("Tabelas existentes destruídas com sucesso.")
# Cria as novas tabelas com base nos modelos definidos em models.py.
Base.metadata.create_all(bind=engine)
print("Novas tabelas (com estrutura atualizada) criadas com sucesso.")

# --- SEEDING (POPULAR COM DADOS INICIAIS) ---

# Abre uma nova sessão com o banco de dados para inserir os dados.
db = SessionLocal()

# Verifica se a tabela de funcionários está vazia para evitar inserir dados duplicados.
# Isto torna o processo de seeding idempotente.
if not db.query(models.Funcionario).first():
    print("Nenhum funcionário encontrado. Inserindo dados iniciais...")

    # --- Criando Funcionários (Exemplos) ---
    # Adapte ou adicione os funcionários reais do salão aqui
    func1 = models.Funcionario(nome='Ana Paula', cargo='Cabeleireira', funcao='Admin',
                               senha_hash=gerar_hash_senha("senha123"))
    func2 = models.Funcionario(nome='Juliana Lima', cargo='Manicure/Pedicure', funcao='Funcionario',
                               senha_hash=gerar_hash_senha("senha123"))
    func3 = models.Funcionario(nome='Carla Gomes', cargo='Esteticista/Depiladora', funcao='Funcionario',
                               senha_hash=gerar_hash_senha("senha123"))
    db.add_all([func1, func2, func3])

    # Lista de serviços formatada para o banco de dados
    servicos_data = [
        # Cabelo
        {'nome': 'Corte Fem', 'duracao_padrao_minutos': 40, 'preco_minimo': '90.00'},
        {'nome': 'Corte Masc', 'duracao_padrao_minutos': 30, 'preco_minimo': '50.00'},
        {'nome': 'Hidratação', 'duracao_padrao_minutos': 40, 'preco_minimo': '100.00'},
        {'nome': 'Nutrição', 'duracao_padrao_minutos': 40, 'preco_minimo': '100.00'},
        {'nome': 'Reconstrução', 'duracao_padrao_minutos': 40, 'preco_minimo': '160.00'},
        {'nome': 'Escova tradicional', 'duracao_padrao_minutos': 30, 'preco_minimo': '65.00'},
        {'nome': 'Escova modelada', 'duracao_padrao_minutos': 40, 'preco_minimo': '70.00'},
        {'nome': 'Escova modelada com baby liss', 'duracao_padrao_minutos': 45, 'preco_minimo': '80.00'},
        {'nome': 'Retoque de raiz', 'duracao_padrao_minutos': 60, 'preco_minimo': '150.00'},
        {'nome': 'Coloração global', 'duracao_padrao_minutos': 60, 'preco_minimo': '190.00'},
        {'nome': 'Aplicação de coloração', 'duracao_padrao_minutos': 60, 'preco_minimo': '80.00'},
        {'nome': 'Mechas', 'duracao_padrao_minutos': 150, 'preco_minimo': '300.00'},
        {'nome': 'Alinhamento capilar', 'duracao_padrao_minutos': 120, 'preco_minimo': '320.00'},
        {'nome': 'Babyliss', 'duracao_padrao_minutos': 5, 'preco_minimo': '50.00'},
        {'nome': 'Lavar / Secar', 'duracao_padrao_minutos': 15, 'preco_minimo': '35.00'},
        # Depilação
        {'nome': 'Sobrancelha', 'duracao_padrao_minutos': 15, 'preco_minimo': '30.00'},
        {'nome': 'Design de sobrancelha', 'duracao_padrao_minutos': 40, 'preco_minimo': '50.00'},
        {'nome': '1/2 perna', 'duracao_padrao_minutos': 20, 'preco_minimo': '30.00'},
        {'nome': 'Virilha', 'duracao_padrao_minutos': 30, 'preco_minimo': '50.00'},
        {'nome': 'Perna inteira', 'duracao_padrao_minutos': 30, 'preco_minimo': '50.00'},
        {'nome': 'Buço', 'duracao_padrao_minutos': 10, 'preco_minimo': '15.00'},
        {'nome': 'Braço', 'duracao_padrao_minutos': 20, 'preco_minimo': '30.00'},
        {'nome': 'Axila', 'duracao_padrao_minutos': 15, 'preco_minimo': '20.00'},
        {'nome': 'Costas', 'duracao_padrao_minutos': 25, 'preco_minimo': '55.00'},
        {'nome': 'Nariz', 'duracao_padrao_minutos': 5, 'preco_minimo': '10.00'},
        {'nome': 'Orelha', 'duracao_padrao_minutos': 10, 'preco_minimo': '20.00'},
        {'nome': 'Queixo', 'duracao_padrao_minutos': 5, 'preco_minimo': '10.00'},
        {'nome': 'Barba', 'duracao_padrao_minutos': 60, 'preco_minimo': '80.00'},
        {'nome': 'Ânus', 'duracao_padrao_minutos': 10, 'preco_minimo': '15.00'},
        # Manicure / Pedicure
        {'nome': 'Pé', 'duracao_padrao_minutos': 30, 'preco_minimo': '35.00'},
        {'nome': 'Mão', 'duracao_padrao_minutos': 30, 'preco_minimo': '30.00'},
        # Podologia
        {'nome': 'Podologia', 'duracao_padrao_minutos': 60, 'preco_minimo': '100.00'},
        # Maquiagem
        {'nome': 'Maquiagem', 'duracao_padrao_minutos': 120, 'preco_minimo': '150.00'},
        {'nome': 'Coloração de sobrancelha', 'duracao_padrao_minutos': 20, 'preco_minimo': '20.00'},
        # Massagem
        {'nome': 'Massagem', 'duracao_padrao_minutos': 120, 'preco_minimo': '90.00'},
        # Limpeza de Pele
        {'nome': 'Limpeza de pele', 'duracao_padrao_minutos': 90, 'preco_minimo': '120.00'},
    ]

    for servico_info in servicos_data:
        novo_servico = models.Servico(
            nome=servico_info['nome'],
            duracao_padrao_minutos=servico_info['duracao_padrao_minutos'],
            preco_minimo=Decimal(servico_info['preco_minimo'])
        )
        db.add(novo_servico)

    # Confirma (commita) todas as inserções de dados na transação.
    db.commit()

    print("Dados iniciais inseridos com sucesso.")
else:
    print("O banco de dados já contém dados. Nenhum dado foi inserido.")

# Fecha a sessão com o banco de dados.
db.close()
