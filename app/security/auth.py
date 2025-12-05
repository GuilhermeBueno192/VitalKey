# app/security/auth.py

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY, ALGORITHM, TEMPO_EXPIRACAO

# endpoint usado pelo FastAPI Docs para login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# cria o token JWT
def criar_token(dados: dict):
    dados_copia = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_EXPIRACAO)
    dados_copia.update({
        "exp": int(expiracao.timestamp()),  # data de expiração
        "sub": dados_copia.get("sub")       # identificador do usuário
    })
    token_jwt = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)
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