# Configurações principais do projeto VitalKey

# Bibliotecas importadas
from dotenv import load_dotenv
import os

# Uso do .env
load_dotenv()  # lê o .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TEMPO_EXPIRACAO = int(os.getenv("TEMPO_EXPIRACAO"))

# Dados do banco MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_PORT = os.getenv("MYSQL_PORT")