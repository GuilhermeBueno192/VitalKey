from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session
from app.security.auth import verificar_token, oauth2_scheme
from app.database import get_db
from app.models.medico import Medico

def autenticar_medico(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        dados_token = verificar_token(token)
        medico_id = dados_token.get("sub")
        if not medico_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if not medico.ativo:
        raise HTTPException(status_code=403, detail="Conta inativa")

    return medico