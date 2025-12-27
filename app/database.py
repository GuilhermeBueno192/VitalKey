from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT

# -------------------------------------------------
# Base declarativa do SQLAlchemy
# Todas as models ORM herdam dessa Base
# -------------------------------------------------
Base = declarative_base()

# -------------------------------------------------
# Definição da URL do banco de dados
# Prioriza MySQL (produção) e cai para SQLite (dev)
# -------------------------------------------------

# Verifica se todas as variáveis de ambiente do MySQL existem
if all([MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT]):
    # Conexão com MySQL usando PyMySQL
    DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
else:
    # Fallback para SQLite em ambiente de desenvolvimento
    print("⚠️  Usando banco local SQLite (modo desenvolvimento)")
    DATABASE_URL = "sqlite:///./vitalkey.db"

# -------------------------------------------------
# Configuração do engine do SQLAlchemy
# -------------------------------------------------

# SQLite exige esse parâmetro para permitir múltiplas threads
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    echo=False,           # Não exibe SQL no console (pode ativar em debug)
    pool_pre_ping=True,   # Verifica se a conexão ainda está válida
    connect_args=connect_args
)

# -------------------------------------------------
# Fábrica de sessões do banco
# -------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------------------------------
# Dependency do FastAPI para acesso ao banco
# -------------------------------------------------
def get_db():
    """
    Cria e fornece uma sessão do banco de dados.
    Garante que a sessão seja fechada ao final da requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()