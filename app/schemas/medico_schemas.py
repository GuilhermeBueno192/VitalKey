from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Usado para CRIAR um médico (contém a senha)
class MedicoCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    especialidade: str = Field(..., min_length=2, max_length=100)
    crm: str = Field(..., min_length=4, max_length=20)
    email: str = Field(..., min_length=5, max_length=255)
    senha: str = Field(..., min_length=4, max_length=100)

    model_config = {
        "from_attributes": True  # substitui orm_mode no Pydantic v2
    }

# Usado para LOGIN (só precisa de CRM e senha)
class MedicoLogin(BaseModel):
    login: str
    senha: str

# Usado para RETORNAR dados (sem expor senha)
class MedicoResponse(BaseModel):
    id: int
    nome: str
    especialidade: str
    crm: str
    email: str
    ativo: bool

    model_config = {
        "from_attributes": True
    }

class MedicoUpdate(BaseModel):
    nome: Optional[str] = None
    especialidade: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None  # pode ser alterada

    model_config = {
        "from_attributes": True
    }

class MedicoAtivoUpdate(BaseModel):
    ativo: bool

    model_config = {
        "from_attributes": True
    }