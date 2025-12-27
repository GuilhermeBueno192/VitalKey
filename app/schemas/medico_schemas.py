from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# ============================
# SCHEMA PARA CRIAÇÃO DE MÉDICO
# ============================
# Usado quando um médico é CADASTRADO no sistema
# Contém a senha, pois ela só existe na criação
class MedicoCreate(BaseModel):
    # Nome completo do médico
    nome: str = Field(..., min_length=2, max_length=100)

    # Especialidade médica (ex: Cardiologia, Pediatria)
    especialidade: str = Field(..., min_length=2, max_length=100)

    # CRM do médico (identificador profissional)
    crm: str = Field(..., min_length=4, max_length=20)

    # Email do médico (único no sistema)
    email: str = Field(..., min_length=5, max_length=255)

    # Senha em texto puro (será criptografada no backend)
    senha: str = Field(..., min_length=4, max_length=100)

    # Permite converter automaticamente ORM → Pydantic
    model_config = {
        "from_attributes": True
    }


# ============================
# SCHEMA PARA LOGIN
# ============================
# Usado exclusivamente para autenticação
# O campo "login" pode ser CRM ou email (dependendo da regra do backend)
class MedicoLogin(BaseModel):
    login: str
    senha: str


# ============================
# SCHEMA DE RESPOSTA (RETORNO)
# ============================
# Usado para DEVOLVER dados do médico para o frontend
# NÃO expõe a senha por segurança
class MedicoResponse(BaseModel):
    id: int
    nome: str
    especialidade: str
    crm: str
    email: str
    ativo: bool  # indica se o médico está ativo no sistema

    model_config = {
        "from_attributes": True
    }


# ============================
# SCHEMA PARA ATUALIZAÇÃO
# ============================
# Usado em PATCH/PUT
# Todos os campos são opcionais, pois a atualização é parcial
class MedicoUpdate(BaseModel):
    nome: Optional[str] = None
    especialidade: Optional[str] = None
    email: Optional[str] = None

    # Senha pode ser alterada, mas não é obrigatória
    senha: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


# ============================
# SCHEMA PARA ATIVAR / DESATIVAR
# ============================
# Usado apenas para controle de status (soft delete)
class MedicoAtivoUpdate(BaseModel):
    # True → ativo | False → inativo
    ativo: bool

    model_config = {
        "from_attributes": True
    }