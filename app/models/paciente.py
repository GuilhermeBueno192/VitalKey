from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# ======================================================
# Modelo principal do Paciente
# ======================================================
class Paciente(Base):
    __tablename__ = "paciente"  # Nome da tabela no banco de dados

    # Identificador único do paciente
    id = Column(Integer, primary_key=True, index=True)

    # Nome completo do paciente
    nome = Column(String(100), nullable=False)

    # Listas armazenadas em formato JSON para maior flexibilidade
    alergias = Column(JSON, default=list)
    doencas_cronicas = Column(JSON, default=list)
    medicamentos_continuos = Column(JSON, default=list)
    contatos_emergencia = Column(JSON, default=list)

    # Data e hora de criação do cadastro
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Indica se o paciente está ativo no sistema
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamento 1:1 com InformacoesPrivadas
    # - uselist=False → garante relação um-para-um
    # - cascade="all, delete" → ao excluir o paciente, exclui os dados privados
    informacoes_privadas = relationship(
        "InformacoesPrivadas",
        back_populates="paciente",
        uselist=False,
        cascade="all, delete"
    )


# ======================================================
# Informações médicas sensíveis do paciente
# ======================================================
class InformacoesPrivadas(Base):
    __tablename__ = "informacoes_privadas"  # Tabela separada para dados sensíveis

    # Identificador único do registro
    id = Column(Integer, primary_key=True, index=True)

    # Chave estrangeira vinculando ao paciente
    paciente_id = Column(
        Integer,
        ForeignKey("paciente.id", ondelete="CASCADE"),
        nullable=False
    )

    # Tipo sanguíneo do paciente (ex: O+, A-, AB+)
    tipo_sanguineo = Column(String(5))

    # Histórico médico armazenado em JSON
    cirurgias = Column(JSON, default=list)
    internacoes_passadas = Column(JSON, default=list)
    alteracoes_exames = Column(JSON, default=list)
    historico_exames = Column(JSON, default=list)

    # Relacionamento inverso com Paciente
    paciente = relationship(
        "Paciente",
        back_populates="informacoes_privadas"
    )