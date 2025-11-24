# app/main.py
from fastapi import FastAPI
from app.routers.medico_router import router as medico_router
from app.routers.paciente_router import router as paciente_router
from app.database import Base, engine

# Cria as tabelas automaticamente (desenvolvimento)
Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI(title="API de Pacientes")

# Inclui as rotas com prefixo e tag
app.include_router(medico_router)
app.include_router(paciente_router)