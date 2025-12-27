from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import text

from app.database import get_db  # função que retorna a sessão do SQLAlchemy
from app.models.paciente import Paciente, InformacoesPrivadas  # SQLAlchemy models
from app.schemas.paciente_schemas import PacienteBase, PacienteResponse, PacienteUpdate, PacienteAtivoUpdate, PacienteCreate
from app.security.dependencies import autenticar_medico

router = APIRouter()

# GET - Pesquisa pacientes ativos por ID e/ou nome (ou retorna todos se não houver filtros)
@router.get("/pacientes", response_model=List[PacienteBase])
def pesquisar_pacientes(id: Optional[int] = None, nome: Optional[str] = None, db: Session = Depends(get_db)
):
    """
    Pesquisa pacientes ativos por ID e/ou nome.
    Se nenhum parâmetro for informado, retorna todos os pacientes ativos.
    """
    
    query = db.query(Paciente).filter(Paciente.ativo == True) # Considera apenas pacientes ativos na pesquisa

    if id is not None:
        query = query.filter(Paciente.id == id)
    if nome:
        query = query.filter(Paciente.nome.ilike(f"%{nome}%"))

    return query.all()

# GET público - Retorna informações básicas de um paciente específico
@router.get("/paciente/{paciente_id}", response_model=PacienteBase)
def get_paciente_publico(paciente_id: str, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == int(paciente_id)).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    return paciente

# GET privado - Retorna informações completas, precisa de token
@router.get("/paciente/{paciente_id}/privado", response_model=PacienteResponse)
def get_paciente_privado(paciente_id: str, db: Session = Depends(get_db), medico=Depends(autenticar_medico)):
    paciente = db.query(Paciente).filter(Paciente.id == int(paciente_id)).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    return paciente

# POST - Cria um novo paciente e, opcionalmente, suas informações privadas
@router.post("/paciente", response_model=PacienteResponse)
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
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

# PATCH - Atualiza parcialmente um paciente e suas informações privadas
@router.patch("/paciente/{id}", response_model=PacienteResponse)
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

# DELETE - Remove permanentemente um paciente pelo ID
@router.delete("/paciente/{id}", status_code=204)
def deletar_paciente(id: int, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == id).first()

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    db.delete(paciente)
    db.commit()

    return