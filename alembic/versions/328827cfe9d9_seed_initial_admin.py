"""seed_initial_admin

Revision ID: 328827cfe9d9
Revises: f8101c303aa4
Create Date: 2026-04-20 21:46:38.387749

"""

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext


revision = '328827cfe9d9'
down_revision = 'f8101c303aa4' 


branch_labels = None
depends_on = None

def upgrade():
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("admin123")

  
    op.execute(
        f"""
        INSERT INTO funcionarios (nome, senha_hash, funcao, is_ativo, saldo_conta_corrente)
        VALUES ('admin', '{hashed_password}', 'Admin', True, 0.0)
        """
    )

def downgrade():
    op.execute("DELETE FROM funcionarios WHERE nome = 'admin'")