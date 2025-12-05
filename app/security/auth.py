# app/security/auth.py

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY, ALGORITHM, TEMPO_EXPIRACAO

# endpoint usado pelo FastAPI Docs para login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# cria o token JWT
def criar_token(medico_id: int):
    """
    Cria um token JWT com o campo 'sub' contendo o id do médico.
    """
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_EXPIRACAO)
    payload = {
        "sub": str(medico_id),  # sempre usar string é mais seguro
        "exp": int(expiracao.timestamp())
    }
    token_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

# verifica se o token ainda é válido
def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        
        return payload
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")