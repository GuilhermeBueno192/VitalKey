# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.medico_router import router as medico_router
from app.routers.paciente_router import router as paciente_router

# Cria a aplicação FastAPI
app = FastAPI(title="API de Pacientes")

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste depois se quiser restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz (necessária para testes e health-check)
@app.get("/")
def root():
    return {"status": "ok"}

# Inclui as rotas
app.include_router(medico_router)
app.include_router(paciente_router)