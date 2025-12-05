from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.config import SECRET_KEY, ALGORITHM
from app.security.auth import verificar_token, oauth2_scheme
from app.database import get_db
from app.models.medico import Medico

def autenticar_medico(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        medico_id = payload.get("sub")
        if medico_id is None:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    # Certifique-se de converter para int se o id no DB for int
    medico = db.query(Medico).filter(Medico.id == int(medico_id)).first()
    if not medico:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    if not medico.ativo:
        raise HTTPException(status_code=403, detail="Conta inativa")
    return medico