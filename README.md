# Bella Estética - Sistema de Gestão para Salão de Beleza

## Descrição

Este projeto é um sistema de gestão web completo para salões de beleza ou barbearias, desenvolvido como o meu primeiro grande projeto de portfólio para a faculdade de Análise e Desenvolvimento de Sistemas. A aplicação foi inspirada pela necessidade real do salão de beleza da minha mãe, que anteriormente gerenciava toda a sua operação com papel e caneta.

O sistema visa modernizar e otimizar a gestão diária, oferecendo uma solução robusta para agendamentos, controle financeiro, gestão de clientes, funcionários e produtos, com uma arquitetura de software limpa e escalável.

## Funcionalidades Principais

- **Autenticação Segura:** Sistema de login com distinção entre utilizadores "Funcionário" e "Admin", protegendo as rotas de acordo com a permissão.
- **Agenda Dinâmica e Unificada:** Interface de agenda centralizada que permite visualizar e alternar entre os horários de múltiplos funcionários, fazer agendamentos e bloquear horários.
- **Gestão Financeira Completa:**
    - **Fluxo de Caixa:** Registo de todas as entradas e saídas com filtros por data e funcionário.
    - **Contas Correntes de Funcionários:** Sistema para gerir débitos e créditos internos (ex: permutas, adiantamentos).
- **Hub de Clientes (CRM):**
    - Cadastro automático (no agendamento) e manual de clientes.
    - Histórico completo de serviços e extrato detalhado de transações de crédito.
    - **Sistema de Venda de Pacotes** de crédito com descontos percentuais.
- ****Gestão e Venda de Produtos:****
    - **CRUD completo de Produtos** na área de administração, com upload de imagens (com validação de tipo e tamanho).
    - **Ponto de Venda (PDV)** para registo de vendas de produtos, com lógica de comissão configurável.
- **Painel de Administração:**
    - Gestão completa de Funcionários (criar, editar, desativar), Serviços e Categorias.
    - Dashboards de desempenho da equipa com filtros personalizáveis.
    - Página de Configurações Gerais para que o administrador possa ajustar as regras de negócio (ex: limite de desconto, comissões) sem precisar de alterar o código.
- **Relatórios e Auditoria:** Logs detalhados de todas as alterações importantes no sistema e dashboards de desempenho individual e de equipa.

## Tecnologias Utilizadas

- **Backend:** Python com FastAPI (utilizando APIRouter para uma arquitetura modular)
- **Banco de Dados:** PostgreSQL
- **ORM e Migrações:** SQLAlchemy e **Alembic**
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Autenticação:** Sessões de Middleware do Starlette com hashing de senhas (Passlib)
- **Segurança:** Variáveis de ambiente com python-dotenv
- **Controlo de Versões:** Git e GitHub

## Metodologia e Agradecimentos

Este projeto foi desenvolvido com uma metodologia de prototipagem rápida e desenvolvimento interativo. A visão para as funcionalidades, a arquitetura do software, a modelagem do banco de dados e todo o processo de depuração e testes foram conduzidos por mim.

Para acelerar a escrita do código e servir como uma ferramenta de aprendizado, utilizei o Google Gemini como um assistente de programação. Esta colaboração permitiu-me focar nos aspetos estratégicos do projeto — como o design do fluxo de trabalho do utilizador e a lógica de negócio — enquanto o Gemini cuidava da implementação técnica.

A capacidade de guiar uma ferramenta de IA para construir uma aplicação complexa e funcional foi uma parte fundamental da minha experiência de aprendizado neste projeto.

## Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e executar a aplicação no seu ambiente local.

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO_NO_GITHUB]
    cd [NOME_DO_SEU_REPOSITORIO]
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # Para Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as variáveis de ambiente:**
    - Crie uma cópia do ficheiro `.env.example` e renomeie-a para `.env`.
    - Edite o ficheiro `.env` com as suas credenciais do PostgreSQL e uma `SECRET_KEY` aleatória.
5.  **Aplique as migrações da base de dados:**
    - Este comando cria e atualiza as tabelas do banco de dados de forma segura.
    ```bash
    alembic upgrade head
    ```
6.  **Inicie o servidor:**
    ```bash
    uvicorn main:app --reload
    ```
A aplicação estará disponível em `http://127.0.0.1:8000`.