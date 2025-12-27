# app/security/auth.py

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_KEY, ALGORITHM, TEMPO_EXPIRACAO

# -------------------------------------------------
# OAuth2PasswordBearer
# -------------------------------------------------
# Define qual endpoint o Swagger (FastAPI Docs)
# vai usar para realizar o login e obter o token
#
# Esse tokenUrl NÃO é a rota protegida,
# é a rota de autenticação (/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# -------------------------------------------------
# Criação do token JWT
# -------------------------------------------------
def criar_token(medico_id: int):
    """
    Cria um token JWT contendo:
    - sub: identificador do médico (id)
    - exp: timestamp de expiração do token
    """

    # Define o horário de expiração do token
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_EXPIRACAO)

    # Payload do JWT
    payload = {
        # 'sub' (subject) identifica quem é o dono do token
        # JWT recomenda que seja string
        "sub": str(medico_id),

        # 'exp' define quando o token expira (em timestamp)
        "exp": int(expiracao.timestamp())
    }

    # Geração do token JWT assinado
    token_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token_jwt


# -------------------------------------------------
# Verificação e validação do token JWT
# -------------------------------------------------
def verificar_token(token: str):
    """
    Verifica se o token JWT é válido, assinado corretamente
    e se não está expirado.

    Retorna o payload decodificado caso seja válido.
    """
    try:
        # Decodifica o token usando a chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verifica se o campo 'sub' existe no payload
        if payload.get("sub") is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido ou expirado"
            )

        # Retorna os dados do token (payload)
        return payload

    # Erro genérico de token inválido, expirado ou adulterado
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )