**Cada integrante do grupo é responsável por um commit específico, mapeado no Plano de Ação. Este guia descreve o fluxo completo: desde preparar o ambiente local até ter o código aceito no repositório oficial.**

---

# Para todos os contribuidores

## Passo 0: Preparação Inicial (Apenas na primeira vez)

Antes de escrever qualquer código, você precisa trazer o projeto para a sua máquina e configurar o ambiente.

**1. Fazer o Fork no GitHub**
Acesse `https://github.com/perinotti/web-beautyparlor-management`. Clique no botão **Fork** no canto superior direito para criar uma cópia do projeto sob o seu próprio usuário.

**2. Clonar o seu Fork**
No terminal, baixe o seu repositório para a sua máquina (substitua `SEU_USUARIO` pelo seu usuário do GitHub):

```r
git clone https://github.com/SEU_USUARIO/web-beautyparlor-management.git
```

**3. Entrar na pasta e abrir a IDE**

Navegue até a pasta que acabou de ser criada e abra seu editor de código (como VSCodium ou VS Code):

```r
cd web-beautyparlor-management
codium .   # ou use 'code .' se estiver utilizando o VS Code padrão
```

**4. Criar e ativar o ambiente virtual (venv)**

Crie o ambiente isolado do Python para não conflitar com outras bibliotecas do seu computador:

```r
python -m venv venv
```

Ative o ambiente virtual usando o comando correspondente ao seu sistema operacional:

| Sistema Operacional | Comando no Terminal |
| --- | --- |
| **Linux / macOS** | `source venv/bin/activate` |
| **Windows** | `venv\Scripts\activate` |

**5. Instalar as dependências**

Com o ambiente ativado, instale as bibliotecas necessárias para o projeto rodar:

```r
pip install -r requirements.txt
```

## Passo 1: Conectar ao repositório principal

Garanta que sua cópia local consegue enxergar e baixar as atualizações feitas por outros desenvolvedores no repositório principal.

**Adicionar o "upstream" (fazer apenas uma vez):**

```bash
# Adicionar o repositório principal como "upstream" (fazer apenas uma vez)
git remote add upstream https://github.com/perinotti/web-beautyparlor-management.git

# Sempre que for começar um trabalho novo, atualize sua main local
git checkout main
git pull upstream main
```

---

## Passo 2. Criar uma branch para o seu trabalho

Nunca trabalhe diretamente na branch `main`. Crie uma branch com um nome descritivo que identifique o commit que você está fazendo.

O padrão de nome é: `tipo/descricao-curta`

```bash
# Exemplos:
git checkout -b fix/crash-pagamento-credito        # Commit 1
git checkout -b fix/imports-deprecados             # Commit 2
git checkout -b fix/remove-create-all-alembic      # Commit 3
git checkout -b fix/status-http-401-login          # Commit 4
```

---

## Passo 3: Fazer as alterações e testar

Faça apenas as alterações descritas no seu commit. Não aproveite para corrigir outras coisas — isso dificulta a revisão e mistura responsabilidades no histórico.

Se você fechou o terminal desde o Passo 0, lembre-se de reativar o ambiente virtual antes de testar:

| Sistema Operacional | Comando no Terminal |
| --- | --- |
| **Linux / macOS** | `source venv/bin/activate` |
| **Windows** | `venv\Scripts\activate` |

Com o ambiente ativado, rode o servidor localmente para testar suas alterações:

```r
uvicorn main:app --reload
```

Verifique se a aplicação sobe sem erros no terminal e se a funcionalidade que você alterou continua funcionando no navegador.

---

### Passo 4. Fazer o commit

Use a mensagem de commit exatamente como definida no Plano de Ação. O padrão utilizado é o **Conventional Commits**, que facilita a leitura do histórico.

```bash
# Adicionar apenas os arquivos que você alterou
git add database.py models.py routers/painel.py

# Commitar com a mensagem definida no plano
git commit -m "fix: corrige imports deprecados, relacionamento quebrado e import duplicado"
```

Evite usar `git add .` — ele adiciona tudo indiscriminadamente e pode incluir arquivos indesejados como o `.env` ou arquivos de cache.

---

### Passo 5. Enviar para o GitHub

```bash
# Enviar sua branch para o GitHub (origin = seu fork)
git push origin fix/imports-deprecados
```

---

### Passo 6. Abrir um Pull Request (PR)

1. Acesse seu repositório no GitHub
2. Clique em **"Compare & pull request"** (aparece automaticamente após o push)
3. Preencha o PR da seguinte forma:

**Título:** igual à mensagem do commit
`fix: corrige imports deprecados, relacionamento quebrado e import duplicado`

**Descrição:** explique o que foi alterado e por quê. Use o seguinte template:

```
## O que foi alterado
- database.py: movido import de `declarative_base` de `sqlalchemy.ext.declarative` (deprecado) para `sqlalchemy.orm`
- models.py: adicionado `back_populates="vendas"` no relacionamento `FluxoCaixa.produto`
- routers/painel.py: removido import duplicado de `collections.defaultdict`

## Por que foi alterado
Correções de qualidade identificadas no mapeamento inicial do projeto. O import deprecado gera avisos no SQLAlchemy moderno e pode quebrar em versões futuras. O `back_populates` faltante causava inconsistência silenciosa no ORM.

## Como testar
1. Rodar `uvicorn main:app --reload`
2. Verificar que nenhum aviso de deprecação aparece no terminal ao iniciar
3. Navegar pelo painel e verificar que produtos carregam normalmente
```

1. Selecione o repositório do dono (`perinotti/web-beautyparlor-management`) como destino
2. Clique em **"Create pull request"**

---

## Para o dono do repositório

### Como revisar um Pull Request

1. Acesse a aba **Pull Requests** no repositório
2. Abra o PR enviado pelo colega
3. Vá na aba **"Files changed"** para ver exatamente o que foi alterado
4. Verifique:
    - As alterações correspondem ao commit descrito no Plano de Ação?
    - Nenhuma outra parte do código foi modificada sem necessidade?
    - A mensagem do commit segue o padrão?
5. Se estiver tudo certo, clique em **"Merge pull request"** → **"Confirm merge"**
6. Se houver algo a corrigir, use a aba **"Review"** para deixar um comentário na linha específica e solicite alterações com **"Request changes"**

### Ordem recomendada para aceitar os PRs

Respeite as dependências definidas no documento "Dependências Importantes":

1. Mergear Commits 1, 2 e 3 antes de qualquer coisa da Fase 2
2. Na Fase 2, mergear Commit 3 antes do Commit 6
3. Nunca mergear Commits 5 e 6 ao mesmo tempo — um por vez

### Como atualizar o repositório local após um merge

```bash
git checkout main
git pull upstream main
```

---

## Resumo do fluxo em uma linha

`Fork` → `Clone` → `pull upstream` → `nova branch` → `alterar` → `testar` → `commit` → `push` → `Pull Request` → `revisão` → `merge`
