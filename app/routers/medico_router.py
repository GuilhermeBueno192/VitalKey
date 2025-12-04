from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db  # função que retorna a sessão do SQLAlchemy
from app.models.medico import Medico  # SQLAlchemy models
from app.schemas.medico_schemas import MedicoCreate, MedicoLogin, MedicoResponse, MedicoUpdate  # Pydantic models
from app.security.auth import criar_token
from app.security.dependencies import autenticar_medico

router = APIRouter()

# GET - Médico logado
@router.get("/me", response_model=MedicoResponse)
def get_me(medico: Medico=Depends(autenticar_medico)):
    return medico

# POST - Criar um novo medico no sistema
@router.post("/medico", response_model=MedicoResponse, status_code=201)
def criar_medico(medico: MedicoCreate, db: Session = Depends(get_db)):
    existente = db.query(Medico).filter(Medico.crm == medico.crm).first()
    if existente:
        raise HTTPException(status_code=400, detail="CRM já cadastrado")

    novo_medico = Medico(**medico.model_dump())  # model_dump() no lugar de .dict() no Pydantic v2
    db.add(novo_medico)
    db.commit()
    db.refresh(novo_medico)
    return novo_medico

# PATCH - Atualizar parcialmente os dados do médico logado
@router.patch("/me", response_model=MedicoResponse)
def atualizar_me(medico_update: MedicoUpdate, medico: Medico = Depends(autenticar_medico), db: Session = Depends(get_db)):
    for field, value in medico_update.model_dump(exclude_unset=True).items():
        setattr(medico, field, value)

    db.commit()
    db.refresh(medico)
    return medico

# DELETE - Remover um médico
@router.delete("/medico/{id}", status_code=204)
def deletar_medico(id: int, db: Session = Depends(get_db)):
    medico = db.query(Medico).filter(Medico.id == id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")

    db.delete(medico)
    db.commit()
    return

# Rota para login com uso do banco de dados
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    medico = db.query(Medico).filter(Medico.crm == form_data.username).first()
    if not medico or medico.senha != form_data.password:
        raise HTTPException(status_code=401, detail="CRM ou senha inválidos")

    token = criar_token({"crm": medico.crm, "id": medico.id})
    return {"access_token": token, "token_type": "bearer"}