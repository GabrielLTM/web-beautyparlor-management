from fastapi import APIRouter, Depends, Request, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from sqlalchemy.orm import Session, joinedload
from collections import defaultdict
from pathlib import Path
from fastapi.templating import Jinja2Templates
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from typing import List

import models
from security import gerar_hash_senha
from dependencies import get_db, get_current_admin_user


router = APIRouter(
    prefix="/painel/admin", # Todas as rotas aqui começarão com /painel/admin
    tags=["Administração"],
    dependencies=[Depends(get_current_admin_user)] # Protege todas as rotas deste router
)


# Configuração dos Templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))



@router.get("/", response_class=HTMLResponse)
async def get_admin_page(request: Request, user: dict = Depends(get_current_admin_user)):
    return templates.TemplateResponse("admin.html", {"request": request, "user": user})


@router.get("/desempenho", response_class=HTMLResponse)
async def get_pagina_desempenho_equipa(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    data_inicio_filtro: date | None = Query(default=None), data_fim_filtro: date | None = Query(default=None)
):
    # ... (código da função get_pagina_desempenho_equipa)
    if data_inicio_filtro and data_fim_filtro:
        data_inicio = data_inicio_filtro
        data_fim = data_fim_filtro
        titulo_periodo = f"Período Personalizado ({data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')})"
    else:
        hoje = date.today()
        weekday_hoje = hoje.weekday()
        offset_para_terca = (weekday_hoje - 1 + 7) % 7
        terca_desta_semana = hoje - timedelta(days=offset_para_terca)
        if weekday_hoje in [3, 4, 5]:
            data_inicio = terca_desta_semana
        else:
            data_inicio = terca_desta_semana - timedelta(days=7)
        data_fim = data_inicio + timedelta(days=4)
        titulo_periodo = f"Semana de Pagamento ({data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')})"
    inicio_periodo = datetime.combine(data_inicio, time.min)
    fim_periodo = datetime.combine(data_fim, time.max)
    funcionarios_ativos = db.query(models.Funcionario).filter(models.Funcionario.is_ativo == True).order_by(models.Funcionario.nome).all()
    desempenho_funcionarios = []
    for func in funcionarios_ativos:
        agendamentos_concluidos = db.query(models.Agendamento).filter(
            models.Agendamento.funcionario_id == func.id,
            models.Agendamento.status == "Concluído",
            models.Agendamento.data_hora.between(inicio_periodo, fim_periodo)
        ).all()
        total_vendas = sum(ag.preco_final for ag in agendamentos_concluidos if ag.preco_final is not None)
        desempenho_funcionarios.append({"funcionario": func, "total_vendas": total_vendas})
    context = {
        "request": request, "user": user, "desempenho_funcionarios": desempenho_funcionarios,
        "titulo_periodo": titulo_periodo, "data_inicio_filtro": data_inicio_filtro,
        "data_fim_filtro": data_fim_filtro
    }
    return templates.TemplateResponse("admin_desempenho.html", context)


@router.get("/fluxo-caixa", response_class=HTMLResponse)
async def get_pagina_fluxo_caixa(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    data_filtro: date | None = Query(default=None), funcionario_id: int | None = Query(default=None)
):
    # ... (código da função get_pagina_fluxo_caixa)
    if data_filtro is None: data_filtro = date.today()
    inicio_do_dia = datetime.combine(data_filtro, time.min)
    fim_do_dia = datetime.combine(data_filtro, time.max)
    funcionarios = db.query(models.Funcionario).order_by(models.Funcionario.nome).all()
    query_caixa = db.query(models.FluxoCaixa).options(
        joinedload(models.FluxoCaixa.funcionario)
    ).filter(models.FluxoCaixa.data_hora_registro.between(inicio_do_dia, fim_do_dia))
    if funcionario_id:
        query_caixa = query_caixa.filter(models.FluxoCaixa.funcionario_id == funcionario_id)
    registros_caixa = query_caixa.order_by(models.FluxoCaixa.data_hora_registro.asc()).all()
    funcionario_selecionado = next((f for f in funcionarios if f.id == funcionario_id), None)
    total_entradas = sum(r.valor for r in registros_caixa if r.tipo == 'Entrada')
    total_saidas = sum(r.valor for r in registros_caixa if r.tipo == 'Saída')
    saldo_do_dia = total_entradas - total_saidas
    context = {
        "request": request, "user": user, "registros": registros_caixa,
        "data_filtro_str": data_filtro.isoformat(),
        "data_exibida_str": data_filtro.strftime("%d/%m/%Y"),
        "total_entradas": total_entradas, "total_saidas": total_saidas,
        "saldo_do_dia": saldo_do_dia, "funcionarios": funcionarios,
        "funcionario_id_filtro": funcionario_id, "funcionario_selecionado": funcionario_selecionado
    }
    return templates.TemplateResponse("admin_fluxo_caixa.html", context)


@router.post("/fluxo-caixa/registrar-saida")
async def handle_form_registrar_saida(
    db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    descricao: str = Form(...), valor: Decimal = Form(...)
):
    # ... (código da função handle_form_registrar_saida)
    nova_saida = models.FluxoCaixa(
        descricao=descricao, valor=valor, tipo="Saída",
        funcionario_id=user['id'], agendamento_id=None
    )
    db.add(nova_saida)
    db.commit()
    return RedirectResponse(
        url=f"/painel/admin/fluxo-caixa?data_filtro={date.today().isoformat()}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/funcionarios", response_class=HTMLResponse)
async def get_pagina_gerir_funcionarios(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)
):
    # ... (código da função get_pagina_gerir_funcionarios)
    funcionarios = db.query(models.Funcionario).order_by(models.Funcionario.nome).all()
    context = {"request": request, "user": user, "funcionarios": funcionarios}
    return templates.TemplateResponse("admin_funcionarios.html", context)


@router.get("/funcionarios/novo", response_class=HTMLResponse)
async def get_pagina_novo_funcionario(
    request: Request, user: dict = Depends(get_current_admin_user)
):
    # ... (código da função get_pagina_novo_funcionario)
    context = {
        "request": request, "user": user, "funcionario": None,
        "action_url": "/painel/admin/funcionarios/novo"
    }
    return templates.TemplateResponse("admin_funcionario_form.html", context)


@router.post("/funcionarios/novo")
async def handle_form_novo_funcionario(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    nome: str = Form(...), cargo: str = Form(...), funcao: str = Form(...), senha: str = Form(...)
):
    # ... (código da função handle_form_novo_funcionario)
    funcionario_existente = db.query(models.Funcionario).filter(models.Funcionario.nome == nome).first()
    if funcionario_existente:
        context = {
            "request": request, "user": user, "funcionario": None,
            "action_url": "/painel/admin/funcionarios/novo",
            "error": "Já existe um funcionário com este nome."
        }
        return templates.TemplateResponse("admin_funcionario_form.html", context, status_code=400)
    senha_hashed = gerar_hash_senha(senha)
    novo_funcionario = models.Funcionario(nome=nome, cargo=cargo, funcao=funcao, senha_hash=senha_hashed)
    db.add(novo_funcionario)
    db.commit()
    return RedirectResponse(url="/painel/admin/funcionarios", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/funcionarios/{funcionario_id}/editar", response_class=HTMLResponse)
async def get_pagina_editar_funcionario(
    request: Request, funcionario_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)
):
    # ... (código da função get_pagina_editar_funcionario)
    funcionario = db.query(models.Funcionario).filter(models.Funcionario.id == funcionario_id).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    context = {
        "request": request, "user": user, "funcionario": funcionario,
        "action_url": f"/painel/admin/funcionarios/{funcionario_id}/editar"
    }
    return templates.TemplateResponse("admin_funcionario_form.html", context)


@router.post("/funcionarios/{funcionario_id}/editar")
async def handle_form_editar_funcionario(
    request: Request, funcionario_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    nome: str = Form(...), cargo: str = Form(...), funcao: str = Form(...), senha: str = Form(None)
):
    # ... (código da função handle_form_editar_funcionario)
    db_funcionario = db.query(models.Funcionario).filter(models.Funcionario.id == funcionario_id).first()
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    db_funcionario.nome = nome
    db_funcionario.cargo = cargo
    db_funcionario.funcao = funcao
    if senha:
        senha_hashed = gerar_hash_senha(senha)
        db_funcionario.senha_hash = senha_hashed
    db.commit()
    return RedirectResponse(url="/painel/admin/funcionarios", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/funcionarios/{funcionario_id}/toggle-status")
async def toggle_status_funcionario(
    funcionario_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)
):
    # ... (código da função toggle_status_funcionario)
    if user['id'] == funcionario_id:
        raise HTTPException(status_code=403, detail="Você não pode desativar sua própria conta.")
    db_funcionario = db.query(models.Funcionario).filter(models.Funcionario.id == funcionario_id).first()
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    db_funcionario.is_ativo = not db_funcionario.is_ativo
    db.commit()
    return RedirectResponse(url="/painel/admin/funcionarios", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/categorias", response_class=HTMLResponse)
async def get_pagina_gerir_categorias(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    error: str = None
):
    # ... (código da função get_pagina_gerir_categorias)
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    context = {"request": request, "user": user, "categorias": categorias, "error": error}
    return templates.TemplateResponse("admin_categorias.html", context)


@router.post("/categorias/nova")
async def handle_form_nova_categoria(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    nome: str = Form(...)
):
    # ... (código da função handle_form_nova_categoria)
    categoria_existente = db.query(models.Categoria).filter(models.Categoria.nome == nome).first()
    if categoria_existente:
        error_message = f"A categoria '{nome}' já existe."
        return await get_pagina_gerir_categorias(request, db, user, error=error_message)
    nova_categoria = models.Categoria(nome=nome)
    db.add(nova_categoria)
    db.commit()
    return RedirectResponse(url="/painel/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/categorias/{categoria_id}/detalhes", response_class=HTMLResponse)
async def get_pagina_detalhes_categoria(
    request: Request, categoria_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)
):
    # ... (código da função get_pagina_detalhes_categoria)
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    todos_os_servicos = db.query(models.Servico).order_by(models.Servico.nome).all()
    context = {"request": request, "user": user, "categoria": categoria, "todos_os_servicos": todos_os_servicos}
    return templates.TemplateResponse("admin_categoria_detalhes.html", context)


@router.post("/categorias/{categoria_id}/detalhes")
async def handle_form_detalhes_categoria(
    request: Request, categoria_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    nome_categoria: str = Form(...), servicos_selecionados: List[int] = Form(default=[])
):
    # ... (código da função handle_form_detalhes_categoria)
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    db_categoria.nome = nome_categoria
    servicos_antigos = db.query(models.Servico).filter(models.Servico.categoria_id == categoria_id).all()
    for servico in servicos_antigos:
        servico.categoria_id = None
    if servicos_selecionados:
        servicos_novos = db.query(models.Servico).filter(models.Servico.id.in_(servicos_selecionados)).all()
        for servico in servicos_novos:
            servico.categoria_id = categoria_id
    db.commit()
    return RedirectResponse(url="/painel/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/categorias/{categoria_id}/excluir")
async def handle_form_excluir_categoria(
    categoria_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)
):
    # ... (código da função handle_form_excluir_categoria)
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    servicos_associados = db.query(models.Servico).filter(models.Servico.categoria_id == categoria_id).all()
    for servico in servicos_associados:
        servico.categoria_id = None
    db.delete(db_categoria)
    db.commit()
    return RedirectResponse(url="/painel/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/servicos", response_class=HTMLResponse)
async def get_pagina_gerir_servicos(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    error: str = None
):
    # ... (código da função get_pagina_gerir_servicos)
    servicos = db.query(models.Servico).order_by(models.Servico.nome).all()
    context = {"request": request, "servicos": servicos, "user": user, "error": error}
    return templates.TemplateResponse("admin_servicos.html", context)


@router.get("/servicos/novo", response_class=HTMLResponse)
async def get_pagina_novo_servico(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)
):
    # ... (código da função get_pagina_novo_servico)
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    context = {"request": request, "user": user, "servico": None, "categorias": categorias}
    return templates.TemplateResponse("admin_servico_form.html", context)


@router.post("/servicos/novo")
async def handle_form_novo_servico(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    nome: str = Form(...), duracao_padrao_minutos: int = Form(...),
    preco_minimo: Decimal = Form(...), categoria_id: int = Form(...)
):
    # ... (código da função handle_form_novo_servico)
    servico_existente = db.query(models.Servico).filter(models.Servico.nome == nome).first()
    if servico_existente:
        error_message = f"O serviço '{nome}' já existe."
        categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
        context = {
            "request": request, "user": user, "servico": None,
            "categorias": categorias, "error": error_message
        }
        return templates.TemplateResponse("admin_servico_form.html", context)
    novo_servico = models.Servico(
        nome=nome, duracao_padrao_minutos=duracao_padrao_minutos,
        preco_minimo=preco_minimo, is_ativo=True, categoria_id=categoria_id
    )
    db.add(novo_servico)
    db.commit()
    return RedirectResponse(url="/painel/admin/servicos", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/servicos/{servico_id}/editar", response_class=HTMLResponse)
async def get_pagina_editar_servico(
    request: Request, servico_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)
):
    # ... (código da função get_pagina_editar_servico)
    servico = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    categorias = db.query(models.Categoria).order_by(models.Categoria.nome).all()
    context = {"request": request, "user": user, "servico": servico, "categorias": categorias}
    return templates.TemplateResponse("admin_servico_form.html", context)


@router.post("/servicos/{servico_id}/editar")
async def handle_form_editar_servico(
    servico_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    nome: str = Form(...), duracao_padrao_minutos: int = Form(...),
    preco_minimo: Decimal = Form(...), categoria_id: int = Form(...)
):
    # ... (código da função handle_form_editar_servico)
    db_servico = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
    if not db_servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    db_servico.nome = nome
    db_servico.duracao_padrao_minutos = duracao_padrao_minutos
    db_servico.preco_minimo = preco_minimo
    db_servico.categoria_id = categoria_id
    db.commit()
    return RedirectResponse(url="/painel/admin/servicos", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/servicos/{servico_id}/excluir")
async def handle_form_excluir_servico(
    request: Request, servico_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)
):
    # ... (código da função handle_form_excluir_servico)
    db_servico = db.query(models.Servico).filter(models.Servico.id == servico_id).first()
    if not db_servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    db_servico.is_ativo = False
    db.commit()
    return RedirectResponse(url="/painel/admin/servicos", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/contas-correntes", response_class=HTMLResponse)
async def get_pagina_contas_correntes(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user)
):
    # ... (código da função get_pagina_contas_correntes)
    funcionarios = db.query(models.Funcionario).filter(models.Funcionario.is_ativo == True).order_by(models.Funcionario.nome).all()
    context = {"request": request, "user": user, "funcionarios": funcionarios}
    return templates.TemplateResponse("admin_contas_correntes.html", context)


@router.get("/contas-correntes/{funcionario_id}", response_class=HTMLResponse)
async def get_pagina_detalhes_conta_corrente(
    request: Request, funcionario_id: int, db: Session = Depends(get_db),
    user: dict = Depends(get_current_admin_user), success: bool = False
):
    # ... (código da função get_pagina_detalhes_conta_corrente)
    funcionario = db.query(models.Funcionario).options(
        joinedload(models.Funcionario.transacoes_conta_corrente)
    ).filter(models.Funcionario.id == funcionario_id).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    context = {"request": request, "user": user, "funcionario": funcionario, "success": success}
    return templates.TemplateResponse("admin_conta_corrente_detalhes.html", context)


@router.post("/contas-correntes/{funcionario_id}/pagamento")
async def handle_form_pagamento_conta_corrente(
    funcionario_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    valor: Decimal = Form(...), descricao: str = Form(...)
):
    # ... (código da função handle_form_pagamento_conta_corrente)
    funcionario = db.query(models.Funcionario).filter(models.Funcionario.id == funcionario_id).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    nova_transacao = models.TransacaoContaCorrente(
        funcionario_id=funcionario_id, admin_id=user['id'], tipo="Crédito",
        valor=valor, descricao=descricao
    )
    db.add(nova_transacao)
    funcionario.saldo_conta_corrente += valor
    db.commit()
    return RedirectResponse(
        url=f"/painel/admin/contas-correntes/{funcionario_id}?success=true",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/configuracoes", response_class=HTMLResponse)
async def get_pagina_configuracoes(
    request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    success: bool = False
):
    # ... (código da função get_pagina_configuracoes)
    limite_desconto_obj = db.query(models.Configuracao).filter(models.Configuracao.chave == "LIMITE_DESCONTO_PACOTE").first()
    limite_desconto = limite_desconto_obj.valor if limite_desconto_obj else "20"
    comissao_permuta_obj = db.query(models.Configuracao).filter(models.Configuracao.chave == "COMISSAO_SALAO_PERMUTA_PERC").first()
    comissao_permuta = comissao_permuta_obj.valor if comissao_permuta_obj else "50"
    context = {
        "request": request, "user": user, "limite_desconto": limite_desconto,
        "comissao_permuta": comissao_permuta, "success": success
    }
    return templates.TemplateResponse("admin_configuracoes.html", context)


@router.post("/configuracoes")
async def handle_form_configuracoes(
    db: Session = Depends(get_db), user: dict = Depends(get_current_admin_user),
    limite_desconto: int = Form(..., ge=0, le=100), comissao_permuta: int = Form(..., ge=0, le=100)
):
    # ... (código da função handle_form_configuracoes)
    def salvar_config(chave: str, valor: str):
        config_obj = db.query(models.Configuracao).filter(models.Configuracao.chave == chave).first()
        if not config_obj:
            config_obj = models.Configuracao(chave=chave, valor=valor)
            db.add(config_obj)
        else:
            config_obj.valor = valor
    salvar_config("LIMITE_DESCONTO_PACOTE", str(limite_desconto))
    salvar_config("COMISSAO_SALAO_PERMUTA_PERC", str(comissao_permuta))
    db.commit()
    return RedirectResponse(url="/painel/admin/configuracoes?success=true", status_code=status.HTTP_303_SEE_OTHER)