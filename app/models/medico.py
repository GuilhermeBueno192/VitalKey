from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# Modelo ORM que representa a tabela de médicos no banco de dados
class Medico(Base):
    __tablename__ = "medicos"  # Nome da tabela no banco

    # Identificador único do médico
    id = Column(Integer, primary_key=True, index=True)

    # Nome completo do médico
    nome = Column(String(100), nullable=False)

    # Especialidade médica (ex: Cardiologia, Endocrinologia)
    especialidade = Column(String(100), nullable=False)

    # CRM do médico (único por profissional)
    crm = Column(String(20), unique=True, nullable=False)

    # Senha de autenticação (armazenada no banco)
    # OBS: em produção, deve ser armazenada como hash
    senha = Column(String(100), nullable=False)

    # E-mail do médico (único)
    email = Column(String(255), unique=True, nullable=False)

    # Indica se o médico está ativo no sistema
    ativo = Column(Boolean, nullable=False, default=True)