from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# =========================================================
# 1. BASES
# Estruturas reutilizáveis usadas em vários schemas
# =========================================================

# ----------------------------
# Contato de emergência
# ----------------------------
# Representa um contato de emergência do paciente
# Será armazenado como JSON no banco
class ContatoEmergencia(BaseModel):
    # Nome da pessoa de contato
    nome: str = Field(..., min_length=2, max_length=100)

    # Telefone do contato
    telefone: str = Field(..., min_length=8, max_length=15)


# ----------------------------
# Informações privadas (BASE)
# ----------------------------
# Dados sensíveis do paciente
# Normalmente ficam em uma tabela separada
class InformacoesPrivadasBase(BaseModel):
    # Tipo sanguíneo (ex: A+, O-, AB+)
    tipo_sanguineo: Optional[str] = Field(None, max_length=5)

    # Histórico médico detalhado
    cirurgias: Optional[List[str]] = Field(default_factory=list)
    internacoes_passadas: Optional[List[str]] = Field(default_factory=list)
    alteracoes_exames: Optional[List[str]] = Field(default_factory=list)
    historico_exames: Optional[List[str]] = Field(default_factory=list)

    # Permite conversão ORM → Pydantic
    class Config:
        from_attributes = True


# ----------------------------
# Paciente base
# ----------------------------
# Estrutura principal do paciente
# Representa dados "não sensíveis"
class PacienteBase(BaseModel):
    # ID vem do banco, por isso é opcional
    id: Optional[int] = None

    # Nome completo do paciente
    nome: str = Field(..., min_length=2, max_length=100)

    # Dados médicos gerais
    alergias: Optional[List[str]] = Field(default_factory=list)
    doencas_cronicas: Optional[List[str]] = Field(default_factory=list)
    medicamentos_continuos: Optional[List[str]] = Field(default_factory=list)

    # Lista de contatos de emergência
    contatos_emergencia: Optional[List[ContatoEmergencia]] = Field(default_factory=list)

    # Data de criação do registro
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


# =========================================================
# 2. CREATE
# Usado no POST /paciente
# Não recebe id nem created_at
# =========================================================

class PacienteCreate(BaseModel):
    # Nome obrigatório
    nome: str = Field(..., min_length=2, max_length=100)

    # Dados médicos iniciais
    alergias: Optional[List[str]] = Field(default_factory=list)
    doencas_cronicas: Optional[List[str]] = Field(default_factory=list)
    medicamentos_continuos: Optional[List[str]] = Field(default_factory=list)

    # Contatos de emergência
    contatos_emergencia: Optional[List[ContatoEmergencia]] = Field(default_factory=list)

    # Informações privadas podem ou não vir na criação
    informacoes_privadas: Optional[InformacoesPrivadasBase] = None


# =========================================================
# 3. UPDATES
# Usados em PATCH / PUT
# Todos os campos são opcionais
# =========================================================

# ----------------------------
# Update de contato de emergência
# ----------------------------
class ContatoEmergenciaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    telefone: Optional[str] = Field(None, min_length=8, max_length=15)


# ----------------------------
# Update de informações privadas
# ----------------------------
class InformacoesPrivadasUpdate(BaseModel):
    tipo_sanguineo: Optional[str] = None
    cirurgias: Optional[List[str]] = None
    internacoes_passadas: Optional[List[str]] = None
    alteracoes_exames: Optional[List[str]] = None
    historico_exames: Optional[List[str]] = None


# ----------------------------
# Update geral do paciente
# ----------------------------
class PacienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    alergias: Optional[List[str]] = None
    doencas_cronicas: Optional[List[str]] = None
    medicamentos_continuos: Optional[List[str]] = None

    # Atualização parcial dos contatos
    contatos_emergencia: Optional[List[ContatoEmergenciaUpdate]] = None

    # Atualização das informações privadas
    informacoes_privadas: Optional[InformacoesPrivadasUpdate] = None


# ----------------------------
# Update de status (soft delete)
# ----------------------------
class PacienteAtivoUpdate(BaseModel):
    # True = ativo | False = inativo
    ativo: bool


# =========================================================
# 4. RESPONSE
# Objeto completo retornado ao frontend
# =========================================================

class PacienteResponse(PacienteBase):
    # Inclui as informações privadas no retorno
    informacoes_privadas: Optional[InformacoesPrivadasBase] = None