# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.medico_router import router as medico_router
from app.routers.paciente_router import router as paciente_router

# -------------------------------------------------
# Criação da aplicação FastAPI
# -------------------------------------------------
# Aqui nasce a API. O título aparece no Swagger (/docs)
app = FastAPI(title="API de Pacientes")

# -------------------------------------------------
# Middleware de CORS
# -------------------------------------------------
# Permite que o frontend (React, Flutter, etc.)
# faça requisições para a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Permite qualquer origem (ideal restringir em produção)
    allow_credentials=True,     # Permite envio de cookies/tokens
    allow_methods=["*"],        # Permite todos os métodos HTTP
    allow_headers=["*"],        # Permite todos os headers
)

# -------------------------------------------------
# Rota raiz (health-check)
# -------------------------------------------------
# Usada para testar se a API está online
@app.get("/")
def root():
    return {"status": "ok"}

# -------------------------------------------------
# Inclusão dos routers da aplicação
# -------------------------------------------------
# Centraliza as rotas por domínio (médico, paciente, etc.)
app.include_router(medico_router)
app.include_router(paciente_router)