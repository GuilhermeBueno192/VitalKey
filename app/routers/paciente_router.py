from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import text

from app.database import get_db  # função que retorna a sessão do SQLAlchemy
from app.models.paciente import Paciente, InformacoesPrivadas  # SQLAlchemy models
from app.schemas.paciente_schemas import PacienteBase, PacienteCompleto, InformacoesPrivadasBase, PacienteUpdate, InformacoesPrivadasUpdate
from app.security.dependencies import autenticar_medico

router = APIRouter()

# GET público: retorna informações básicas de um paciente específico
@router.get("/paciente/{id}", response_model=PacienteBase)
def get_paciente(id: int, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

# GET privado: retorna informações completas, precisa de token
@router.get("/paciente/{paciente_id}/completo", response_model=PacienteCompleto)
def get_paciente_completo(paciente_id: int, db: Session = Depends(get_db), medico=Depends(autenticar_medico)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

# POST - Criar um novo paciente no sistema
@router.post("/paciente", response_model=PacienteCompleto)
def criar_paciente(paciente: PacienteCompleto, db: Session = Depends(get_db)):
    """
    Cria um novo paciente junto com as informações privadas.
    """

    # Cria o objeto Paciente ORM
    novo_paciente = Paciente(
        nome=paciente.nome,
        alergias=paciente.alergias,
        doencas_cronicas=paciente.doencas_cronicas,
        medicamentos_continuos=paciente.medicamentos_continuos,
        contatos_emergencia=[c.model_dump() for c in (paciente.contatos_emergencia or [])]
    )

    # Cria o objeto InformacoesPrivadas ORM, se informado
    if paciente.informacoes_privadas:
        info_privada = InformacoesPrivadas(
            tipo_sanguineo=paciente.informacoes_privadas.tipo_sanguineo,
            cirurgias=paciente.informacoes_privadas.cirurgias,
            internacoes_passadas=paciente.informacoes_privadas.internacoes_passadas,
            alteracoes_exames=paciente.informacoes_privadas.alteracoes_exames,
            historico_exames=paciente.informacoes_privadas.historico_exames
        )
        # Faz a ligação automática pelo relationship
        novo_paciente.informacoes_privadas = info_privada

    # Adiciona e comita no banco
    db.add(novo_paciente)
    db.commit()
    db.refresh(novo_paciente)  # Atualiza o objeto com o ID gerado pelo banco

    return novo_paciente

# PATCH - Atualizar parcialmente um paciente
@router.patch("/paciente/{id}", response_model=PacienteCompleto)
def atualizar_paciente(id: int, paciente_update: PacienteUpdate, db: Session = Depends(get_db)):
    """
    Atualiza parcialmente um paciente e suas informações privadas.
    Campos não enviados permanecem inalterados.
    """
    paciente = db.query(Paciente).filter(Paciente.id == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    # Atualiza campos básicos enviados
    for field, value in paciente_update.model_dump(exclude_unset=True).items():
        if field != "informacoes_privadas":
            setattr(paciente, field, value)

    # Atualiza informações privadas se fornecidas
    if paciente_update.informacoes_privadas:
        if paciente.informacoes_privadas:
            info = paciente.informacoes_privadas
        else:
            info = InformacoesPrivadas()
            paciente.informacoes_privadas = info

        for field, value in paciente_update.informacoes_privadas.model_dump(exclude_unset=True).items():
            setattr(info, field, value)

    db.commit()
    db.refresh(paciente)
    return paciente

# DELETE - Remover um paciente
@router.delete("/paciente/{id}", status_code=204)
def deletar_paciente(id: int, db: Session = Depends(get_db)):
    """
    Deleta um paciente e suas informações privadas automaticamente.
    """

    paciente = db.query(Paciente).filter(Paciente.id == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    db.delete(paciente)  # remove paciente + informações privadas (cascade)
    db.commit()
    return