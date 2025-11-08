# app/main.py
from fastapi import FastAPI
from routes import router
from database import Base, engine

# Cria as tabelas automaticamente (desenvolvimento)
Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI(title="API de Pacientes")

# Inclui as rotas com prefixo e tag
app.include_router(router)