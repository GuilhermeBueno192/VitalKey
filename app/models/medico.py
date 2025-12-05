from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    especialidade = Column(String(100), nullable=False)
    crm = Column(String(20), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)  
    email = Column(String(255), unique=True, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)