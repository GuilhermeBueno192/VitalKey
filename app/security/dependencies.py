from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.config import SECRET_KEY, ALGORITHM
from app.security.auth import verificar_token, oauth2_scheme
from app.database import get_db
from app.models.medico import Medico

def autenticar_medico(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency responsável por:
    - Validar o token JWT
    - Extrair o ID do médico (sub)
    - Buscar o médico no banco
    - Verificar se a conta está ativa

    Retorna o objeto Medico autenticado.
    """

    # -----------------------------
    # Decodificação e validação do JWT
    # -----------------------------
    try:
        # Decodifica o token usando a chave secreta e algoritmo definidos
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Recupera o ID do médico armazenado no campo 'sub'
        medico_id = payload.get("sub")

        # Se não houver 'sub', o token é inválido
        if medico_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido ou expirado"
            )

    # Erro caso o token esteja expirado, adulterado ou inválido
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    # -----------------------------
    # Validação do médico no banco
    # -----------------------------

    # Converte o ID para inteiro (DB usa int)
    medico = db.query(Medico).filter(Medico.id == int(medico_id)).first()

    # Se o médico não existir no banco
    if not medico:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    # Se o médico existir, mas estiver inativo
    if not medico.ativo:
        raise HTTPException(
            status_code=403,
            detail="Conta inativa"
        )

    # Retorna o médico autenticado
    return medico