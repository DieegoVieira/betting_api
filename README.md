# API de Lutas - Sistema Distribuído de Apostas

Microserviço responsável pelo gerenciamento de lutas dentro de um ecossistema distribuído de apostas.

A API implementa:

- CRUD de lutas
- Integração distribuída com API de lutadores
- Segurança M2M via RSA
- Publicação de eventos RabbitMQ
- Arquitetura orientada a eventos
- Persistência PostgreSQL

---

# Tecnologias Utilizadas

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- RabbitMQ
- Neon Database
- Vercel
- Railway
- JWT
- RSA-PSS

---

# Arquitetura

```text
Frontend
   |
Integrador / Gateway
   |
API de Lutas
   |
   +--> PostgreSQL (Neon)
   |
   +--> API de Lutadores
   |
   +--> RabbitMQ
```

---

# Instalação Local

## 1. Clonar repositório

```bash
git clone URL_DO_REPOSITORIO
```

---

## 2. Entrar na pasta

```bash
cd api_lutas
```

---

## 3. Criar ambiente virtual

```bash
python -m venv venv
```

---

## 4. Ativar ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 5. Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Variáveis de Ambiente

Crie um arquivo `.env`:

```env
DATABASE_URL=
POSTGRES_URL_NON_POOLING=
SENHA_ADMIN=
RABBITMQ_URL=
```

---

# Executar Localmente

```bash
uvicorn API_lutas:app --reload
```

Acesse:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Deploy Online

## PostgreSQL

Banco hospedado no:

- Neon

---

## RabbitMQ

RabbitMQ hospedado no:

- Railway

---

## API

Deploy realizado na:

- Vercel

---

# RabbitMQ

A API publica eventos assíncronos na fila:

```text
eventos_lutas
```

Eventos publicados:

| Evento | Descrição |
|---|---|
| luta_criada | Nova luta cadastrada |
| luta_editada | Luta alterada |
| luta_cancelada | Luta removida |

---

# Estrutura do Projeto

```text
.
├── API_lutas.py
├── models.py
├── security.py
├── acess_log.py
├── rabbitmq_service.py
├── requirements.txt
├── vercel.json
├── LICENSE
└── README.md
```

---

# Arquivos Sensíveis

NÃO subir no GitHub:

- `.env`
- `private_key.pem`
- credenciais
- tokens
- URLs privadas

---

# .gitignore

```gitignore
.env
private_key.pem
__pycache__/
*.pyc
venv/
```

---

# Como Subir no GitHub

```bash
git add .
git commit -m "feat: adiciona RabbitMQ e melhorias distribuídas"
git push
```

---

# Conceitos de Sistemas Distribuídos Aplicados

- Microsserviços
- API Gateway
- Comunicação REST
- Comunicação assíncrona
- RabbitMQ / AMQP
- Arquitetura orientada a eventos
- Segurança distribuída
- RSA
- JWT
- Persistência distribuída
- Cloud Computing
- Serverless

---

# 👨‍💻 Autores

* João Pedro Silva da Rosa Lima
* Armando Alves de Oliveira Braga
* Sophia Ishii Dognani