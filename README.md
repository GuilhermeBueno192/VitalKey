# 🧠 Sistema de Gerenciamento de Pacientes

Um sistema backend em **FastAPI** conectado a um banco de dados **SQLite/MySQL**, responsável por gerenciar pacientes, médicos e autenticação com JWT.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.12+**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **SQLite/MySQL**
- **JWT (Auth com JOSE)**

---

## 📂 Estrutura do Projeto

```
app/
├── __init__.py
├── main.py
├── config.py
├── database.py
├── auth/
│   ├── __init__.py
│   ├── auth.py
│   └── dependencies.py
├── models/
│   ├── __init__.py
│   ├── paciente.py
│   └── medico.py
├── routes/
│   ├── __init__.py
│   ├── paciente_routes.py
│   └── medico_routes.py
├── schemas/
│   ├── __init__.py
│   ├── paciente_schema.py
│   └── medico_schema.py
└── utils/
    ├── __init__.py
```

---

## ⚙️ Configuração do Ambiente

Crie um arquivo `.env` com as variáveis de ambiente:

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
TEMPO_EXPIRACAO=60
```

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

## 📋 Exemplos de Requisições

### 🔹 POST `/pacientes/`

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

### 🔹 PATCH `/pacientes/{id}`

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
*.db
__pycache__/
*.pyc
```

---

## 🧠 Desenvolvido por

**Guilherme Bueno** — Projeto acadêmico de Engenharia de Computação  
Integrando conceitos de **banco de dados, autenticação e APIs RESTful**.
