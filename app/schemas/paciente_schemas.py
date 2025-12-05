from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# =========================================================
# 1. BASES (estruturas fundamentais usadas em vários schemas)
# =========================================================

# Listas complexas (JSON)
class ContatoEmergencia(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    telefone: str = Field(..., min_length=8, max_length=15)

class InformacoesPrivadasBase(BaseModel):
    tipo_sanguineo: Optional[str] = Field(None, max_length=5)
    cirurgias: Optional[List[str]] = Field(default_factory=list)
    internacoes_passadas: Optional[List[str]] = Field(default_factory=list)
    alteracoes_exames: Optional[List[str]] = Field(default_factory=list)
    historico_exames: Optional[List[str]] = Field(default_factory=list)

    class Config:
        from_attributes = True

# Paciente básico com informações que vêm do BD
class PacienteBase(BaseModel):
    id: Optional[int] = None
    nome: str = Field(..., min_length=2, max_length=100)
    alergias: Optional[List[str]] = Field(default_factory=list)
    doencas_cronicas: Optional[List[str]] = Field(default_factory=list)
    medicamentos_continuos: Optional[List[str]] = Field(default_factory=list)
    contatos_emergencia: Optional[List[ContatoEmergencia]] = Field(default_factory=list)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


# =========================================================
# 2. CREATE (dados exigidos no POST — sem id, sem created_at)
# =========================================================

class PacienteCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    alergias: Optional[List[str]] = Field(default_factory=list)
    doencas_cronicas: Optional[List[str]] = Field(default_factory=list)
    medicamentos_continuos: Optional[List[str]] = Field(default_factory=list)
    contatos_emergencia: Optional[List[ContatoEmergencia]] = Field(default_factory=list)
    informacoes_privadas: Optional[InformacoesPrivadasBase] = None


# =========================================================
# 3. UPDATES (PATCH/PUT — tudo opcional)
# =========================================================

class ContatoEmergenciaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    telefone: Optional[str] = Field(None, min_length=8, max_length=15)

class InformacoesPrivadasUpdate(BaseModel):
    tipo_sanguineo: Optional[str] = None
    cirurgias: Optional[List[str]] = None
    internacoes_passadas: Optional[List[str]] = None
    alteracoes_exames: Optional[List[str]] = None
    historico_exames: Optional[List[str]] = None

class PacienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    alergias: Optional[List[str]] = None
    doencas_cronicas: Optional[List[str]] = None
    medicamentos_continuos: Optional[List[str]] = None
    contatos_emergencia: Optional[List[ContatoEmergenciaUpdate]] = None
    informacoes_privadas: Optional[InformacoesPrivadasUpdate] = None

class PacienteAtivoUpdate(BaseModel):
    ativo: bool


# =========================================================
# 4. RESPONSE (objeto completo retornado ao front)
# =========================================================

class PacienteResponse(PacienteBase):
    informacoes_privadas: Optional[InformacoesPrivadasBase] = None