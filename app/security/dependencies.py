from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session
from app.security.auth import verificar_token, oauth2_scheme
from app.database import get_db
from app.models import Medico

def autenticar_medico(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Verifica o token JWT e retorna o médico autenticado.
    """
    try:
        dados_token = verificar_token(token)
        crm = dados_token.get("crm")
        if not crm:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    medico = db.query(Medico).filter(Medico.crm == crm).first()
    if not medico:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return medico