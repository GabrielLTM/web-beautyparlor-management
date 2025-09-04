from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# Tabela de Configurações Gerais
class Configuracao(Base):
    __tablename__ = "configuracoes"
    chave = Column(String, primary_key=True)
    valor = Column(String, nullable=False)


# Tabela para as categorias de serviços
class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    servicos = relationship("Servico", back_populates="categoria")


# Tabela para os clientes do salão
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    whatsapp = Column(String, unique=True, index=True)
    saldo_credito = Column(Numeric(10, 2), nullable=False, default=0.0)
    agendamentos = relationship("Agendamento", back_populates="cliente")
    transacoes_credito = relationship("TransacaoCredito", back_populates="cliente", order_by="desc(TransacaoCredito.data_hora)")


# Tabela para os funcionários do salão
class Funcionario(Base):
    __tablename__ = "funcionarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cargo = Column(String)
    senha_hash = Column(String)
    funcao = Column(String, default="Funcionario", nullable=False)
    is_ativo = Column(Boolean, default=True, nullable=False)
    saldo_conta_corrente = Column(Numeric(10, 2), nullable=False, default=0.0)
    agendamentos = relationship("Agendamento", back_populates="funcionario")
    bloqueios = relationship("Bloqueio", back_populates="funcionario")
    transacoes_credito_processadas = relationship("TransacaoCredito", back_populates="funcionario")

    # ### CORREÇÃO AQUI ###
    # Especificamos explicitamente qual chave estrangeira usar para esta relação.
    transacoes_conta_corrente = relationship(
        "TransacaoContaCorrente",
        back_populates="funcionario",
        foreign_keys="[TransacaoContaCorrente.funcionario_id]",
        order_by="desc(TransacaoContaCorrente.data_hora)"
    )


# Tabela para os serviços oferecidos
class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    duracao_padrao_minutos = Column(Integer)
    preco_minimo = Column(Numeric(10, 2))
    is_ativo = Column(Boolean, default=True, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="servicos")


# Tabela para registrar os agendamentos feitos
class Agendamento(Base):
    __tablename__ = "agendamentos"
    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, index=True)
    duracao_efetiva_minutos = Column(Integer)
    preco_final = Column(Numeric(10, 2))
    status = Column(String, default="Agendado", index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"))
    servico_id = Column(Integer, ForeignKey("servicos.id"))
    cliente = relationship("Cliente", back_populates="agendamentos")
    funcionario = relationship("Funcionario", back_populates="agendamentos")
    servico = relationship("Servico")
    transacao_credito_associada = relationship("TransacaoCredito", back_populates="agendamento", uselist=False)
    transacao_conta_corrente_associada = relationship("TransacaoContaCorrente", back_populates="agendamento", uselist=False)


# Tabela para transações de crédito do cliente
class TransacaoCredito(Base):
    __tablename__ = "transacoes_credito"
    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, default=datetime.now)
    tipo = Column(String, index=True)
    valor = Column(Numeric(10, 2), nullable=False)
    descricao = Column(String)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    agendamento_id = Column(Integer, ForeignKey("agendamentos.id"), nullable=True)
    cliente = relationship("Cliente", back_populates="transacoes_credito")
    funcionario = relationship("Funcionario", back_populates="transacoes_credito_processadas")
    agendamento = relationship("Agendamento", back_populates="transacao_credito_associada")


# Tabela para transações da conta corrente do funcionário
class TransacaoContaCorrente(Base):
    __tablename__ = "transacoes_conta_corrente"
    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, default=datetime.now)
    tipo = Column(String, index=True)
    valor = Column(Numeric(10, 2), nullable=False)
    descricao = Column(String)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    agendamento_id = Column(Integer, ForeignKey("agendamentos.id"), nullable=True)
    admin_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)

    # ### CORREÇÃO AQUI ###
    # Especificamos qual chave estrangeira esta relação deve usar para voltar ao funcionário.
    funcionario = relationship("Funcionario", back_populates="transacoes_conta_corrente", foreign_keys=[funcionario_id])
    agendamento = relationship("Agendamento", back_populates="transacao_conta_corrente_associada")


# Tabela para os bloqueios de tempo na agenda
class Bloqueio(Base):
    __tablename__ = "bloqueios"
    id = Column(Integer, primary_key=True, index=True)
    inicio = Column(DateTime)
    fim = Column(DateTime)
    motivo = Column(String, nullable=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"))
    funcionario = relationship("Funcionario", back_populates="bloqueios")


# Tabela para a trilha de auditoria
class LogAlteracao(Base):
    __tablename__ = "logs_alteracoes"
    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(DateTime, default=datetime.now)
    agendamento_id = Column(Integer, ForeignKey("agendamentos.id"))
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"))
    campo_alterado = Column(String)
    valor_antigo = Column(String)
    valor_novo = Column(String)
    funcionario = relationship("Funcionario")
    agendamento = relationship("Agendamento")


# Tabela para registrar o fluxo de caixa
class FluxoCaixa(Base):
    __tablename__ = "fluxo_caixa"
    id = Column(Integer, primary_key=True, index=True)
    data_hora_registro = Column(DateTime, default=datetime.now, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    tipo = Column(String, index=True, nullable=False)
    metodo_pagamento = Column(String, nullable=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"))
    agendamento_id = Column(Integer, ForeignKey("agendamentos.id"), nullable=True)
    funcionario = relationship("Funcionario")
    agendamento = relationship("Agendamento")
