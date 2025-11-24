from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Modelos para listas complexas (JSON)
class ContatoEmergencia(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    telefone: str = Field(..., min_length=8, max_length=15)

# Modelo base do paciente
class PacienteBase(BaseModel):
    id: Optional[int] = None
    nome: str = Field(..., min_length=2, max_length=100)
    alergias: Optional[List[str]] = []
    doencas_cronicas: Optional[List[str]] = []
    medicamentos_continuos: Optional[List[str]] = []
    contatos_emergencia: Optional[List[ContatoEmergencia]] = []
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True

# Modelo para informações privadas
class InformacoesPrivadasBase(BaseModel):
    tipo_sanguineo: Optional[str] = Field(None, max_length=5)
    cirurgias: Optional[List[str]] = []
    internacoes_passadas: Optional[List[str]] = []
    alteracoes_exames: Optional[List[str]] = []
    historico_exames: Optional[List[str]] = []

    class Config:
        from_attributes = True

# Modelo completo combinando paciente + informações privadas
class PacienteCompleto(PacienteBase):
    informacoes_privadas: Optional[InformacoesPrivadasBase] = None


# Opcionais para PATCH

class ContatoEmergenciaUpdate(BaseModel):
    nome: str | None = Field(None, min_length=2, max_length=100)
    telefone: str | None = Field(None, min_length=8, max_length=15)

class InformacoesPrivadasUpdate(BaseModel):
    tipo_sanguineo: Optional[str] = None
    cirurgias: Optional[List[str]] = None
    internacoes_passadas: Optional[List[str]] = None
    alteracoes_exames: Optional[List[str]] = None
    historico_exames: Optional[List[str]] = None

class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    alergias: Optional[List[str]] = None
    doencas_cronicas: Optional[List[str]] = None
    medicamentos_continuos: Optional[List[str]] = None
    contatos_emergencia: Optional[List[ContatoEmergenciaUpdate]] = None
    informacoes_privadas: Optional[InformacoesPrivadasUpdate] = None