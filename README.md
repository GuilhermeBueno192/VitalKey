# 🧠 VitalKey - Sistema de Gerenciamento de Pacientes

Um sistema backend em **FastAPI** conectado a um banco de dados **SQLite/MySQL**, responsável por gerenciar pacientes, médicos e autenticação com JWT.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.12+**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **MySQL (produção com PyMySQL)**
- **SQLite (somente para testes locais)**
- **JWT (Auth com JOSE)**
- **Python-multipart**

---

## 📂 Estrutura do Projeto

```
VitalKey/
│── main.py
│── requirements.txt
│── README.md
└── app/
    ├── database.py
    ├── config.py
    ├── __init__.py
    ├── models/
    │   ├── medico.py
    │   └── paciente.py
    ├── routers/
    │   ├── medico_router.py
    │   └── paciente_router.py
    ├── schemas/
    │   ├── medico_schemas.py
    │   └── paciente_schemas.py
    ├── security/
    │   ├── auth.py
    │   └── dependencies.py
    └── utils/
        └── __init__.py
```

---

## ⚙️ **Configuração do Ambiente**

Crie um arquivo `.env` na raiz do projeto contendo:

``` env
DATABASE_URL=mysql+pymysql://usuario:senha@host:3306/nome_do_banco
SECRET_KEY=chave_super_secreta
ALGORITHM=HS256
TEMPO_EXPIRACAO=60
```

### Para testes locais com SQLite:

``` env
DATABASE_URL=sqlite:///./teste.db
```

---

## ▶️ **Como Rodar o Projeto**

1.  Instale as dependências:

``` bash
pip install -r requirements.txt
```

2.  Execute o servidor:

``` bash
uvicorn main:app --reload
```

3.  Acesse a documentação automática:

```{=html}
<!-- -->
```
    http://localhost:8000/docs
    
---

## 🧩 Endpoints Principais

| **Método** | **Endpoint**              | **Descrição**                                                            |
| ---------- | ------------------------- | ------------------------------------------------------------------------ |
| **POST**   | `/medico/`                | Cria um novo médico no sistema                                           |
| **POST**   | `/login`                  | Autentica o médico e gera um token JWT                                   |
| **POST**   | `/paciente/`              | Cria um novo paciente com informações públicas e privadas                |
| **GET**    | `/medico/{id}`            | Lista o médico cadastrado                                                |
| **GET**    | `/paciente/{id}`          | Lista o paciente mostrando apenas dados públicos                         |
| **GET**    | `/paciente/{id}/completo` | Lista o paciente com dados completos (somente para médicos autenticados) |
| **PATCH**  | `/medico/{id}`            | Atualiza parcialmente os dados de um médico                              |
| **PATCH**  | `/paciente/{id}`          | Atualiza parcialmente os dados de um paciente                            |
| **DELETE** | `/medico/{id}`            | Exclui um médico existente                                               |
| **DELETE** | `/paciente/{id}`          | Exclui um paciente existente                                             |

---

## 🔐 **Autenticação**

Após o login, envie o token nos headers:

    Authorization: Bearer <seu_token_jwt>

---

## 📋 Exemplos de Requisições

### 🔹 POST `/paciente/`

```json
{
  "nome": "Ana Clara",
  "alergias": ["poeira"],
  "doencas_cronicas": ["asma"],
  "medicamentos_continuos": ["ventolin"],
  "contatos_emergencia": [{ "nome": "Maria Clara", "telefone": "11999999999" }],
  "informacoes_privadas": {
    "tipo_sanguineo": "B+",
    "cirurgias": ["apendicectomia"],
    "internacoes_passadas": [],
    "alteracoes_exames": [],
    "historico_exames": []
  }
}
```

### 🔹 PATCH `/paciente/{id}`

```json
{
  "nome": "Ana Clara Souza",
  "informacoes_privadas": {
    "tipo_sanguineo": "B+"
  }
}
```

### 🔹 POST `/login`

```json
{
  "crm": "123456-SP",
  "senha": "SenhaTeste123!"
}
```

---

## 🔑 Exemplo de Token JWT

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## ⚠️ .gitignore

Certifique-se de **não versionar** arquivos sensíveis. Seu `.gitignore` deve conter:

```
.env
__pycache__/
*.pyc
```

---

## 🧠 Desenvolvido por

**Guilherme Bueno** — Projeto acadêmico de Engenharia de Computação  
Aplicando conceitos de **APIs REST**, **bancos de dados**, **segurança**
e **autenticação JWT**.

