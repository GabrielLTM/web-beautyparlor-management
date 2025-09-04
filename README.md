Sistema de Gestão para Salão de Beleza

Sobre o projeto:

Este projeto é um sistema de gestão web completo para salões de beleza, desenvolvido como o meu primeiro grande projeto de portfólio para a faculdade de Análise e Desenvolvimento de Sistemas. A aplicação foi inspirada pela necessidade real do salão de beleza da minha mãe, que anteriormente gerenciava toda a sua operação com papel e caneta.

O sistema visa modernizar e otimizar a gestão diária, oferecendo uma solução robusta para agendamentos, controle financeiro, gestão de clientes e desempenho da equipe, com uma arquitetura de software limpa e escalável.

Funcionalidades principais:

    Autenticação segura: sistema de login com distinção entre utilizadores "Funcionário" e "Admin", protegendo as rotas de acordo com a permissão.

    Agenda dinâmica e unificada: uma interface de agenda centralizada, que permite visualizar e alternar entre os horários de múltiplos funcionários em tempo real, sem recarregar a página, otimizando o processo de agendamento.

    Gestão financeira completa:

        Fluxo de caixa: registro de todas as entradas e saídas de dinheiro com filtros por data e funcionário.

        Contas correntes de funcionários: um sistema robusto para gerenciar débitos e créditos internos, permitindo o registro de pagamentos complexos como permutas, sem comprometer a integridade do fluxo de caixa.

    Hub de clientes (CRM):

        Cadastro automático e manual de clientes.

        Histórico completo de serviços e extrato detalhado de transações de crédito.

        Sistema de venda de pacotes de crédito com descontos percentuais, limitado por uma regra de negócio configurável pelo administrador.

    Painel de administração:

        Gestão completa de funcionários (criar, editar, desativar), serviços e categorias.

        Dashboards de desempenho da equipe com filtros personalizáveis.

        Página de configurações gerais para que o administrador possa ajustar as regras de negócio (ex: limite de desconto, comissão de permuta) sem precisar alterar o código.

Tecnologias Utilizadas

    Backend: Python com FastAPI (utilizando APIRouter para uma arquitetura modular)

    Banco de dados: PostgreSQL

    ORM: SQLAlchemy

    Frontend: HTML5, CSS3, Bootstrap 5, JavaScript

    Autenticação: sessões de Middleware do Starlette com hashing de senhas (Passlib)

    Segurança: variáveis de ambiente com python-dotenv

    Controle de versões: Git e GitHub

Como executar o projeto localmente

Siga os passos abaixo para configurar e executar a aplicação no seu ambiente local.

1. Clone o repositório:

git clone [URL_DO_SEU_REPOSITORIO_NO_GITHUB]
cd [NOME_DO_SEU_REPOSITORIO]

2. Crie e ative um ambiente virtual:

# Para Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Para Windows
python -m venv .venv
.venv\Scripts\activate

3. Instale as dependências:

O projeto utiliza um ficheiro requirements.txt para gerar as dependências.

pip install -r requirements.txt

4. Configure as variáveis de ambiente:

Crie uma cópia do ficheiro .env.example e renomeie-a para .env. Depois, edite o ficheiro .env com as suas credenciais do PostgreSQL.

# Exemplo do conteúdo do ficheiro .env

DATABASE_URL="postgresql://seu_usuario:sua_senha@localhost/seu_banco"
SECRET_KEY="uma_chave_secreta_muito_forte_e_aleatoria"

5. Inicialize o banco de dados:

Execute o script para criar todas as tabelas e inserir os dados iniciais.

python init_db.py

6. Inicie o servidor:

Com tudo configurado, inicie o servidor de desenvolvimento.

uvicorn main:app --reload

A aplicação estará disponível em http://127.0.0.1:8000.