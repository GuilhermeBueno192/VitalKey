from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Paciente(Base):
    __tablename__ = "paciente"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    alergias = Column(JSON, default=[])
    doencas_cronicas = Column(JSON, default=[])
    medicamentos_continuos = Column(JSON, default=[])
    contatos_emergencia = Column(JSON, default=[])
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    informacoes_privadas = relationship(
        "InformacoesPrivadas",
        back_populates="paciente",
        uselist=False,
        cascade="all, delete"
    )

class InformacoesPrivadas(Base):
    __tablename__ = "informacoes_privadas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("paciente.id", ondelete="CASCADE"), nullable=False)
    tipo_sanguineo = Column(String(5))
    cirurgias = Column(JSON, default=[])
    internacoes_passadas = Column(JSON, default=[])
    alteracoes_exames = Column(JSON, default=[])
    historico_exames = Column(JSON, default=[])

    paciente = relationship("Paciente", back_populates="informacoes_privadas")