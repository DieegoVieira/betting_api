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

# 🔗 Acesso Público

**Repositório (Fork):** https://github.com/DieegoVieira/betting_api.git

**URL de Produção:**

```
https://betting-api-lutas.vercel.app
```

**Swagger (documentação interativa):**

```
https://betting-api-lutas.vercel.app/docs
```

---

# 📌 Endpoints Disponíveis

| Método | Rota | Proteção | Descrição |
|--------|------|----------|-----------|
| GET | `/` | Pública | Verifica status da API |
| POST | `/admin/cadastrar-integrador` | X-Admin-Token | Cadastra um integrador autorizado |
| GET | `/lutas/` | RSA | Lista todas as lutas |
| POST | `/lutas/` | RSA | Cria uma nova luta |
| PUT | `/lutas/{id}` | RSA | Edita uma luta existente |
| DELETE | `/lutas/{id}` | RSA | Cancela (remove) uma luta |

---

# 🔐 Autenticação

As rotas protegidas por RSA exigem dois headers obrigatórios:

| Header | Descrição |
|--------|-----------|
| `x-api-nome` | Nome do integrador cadastrado |
| `x-assinatura` | Assinatura RSA-PSS em Base64 |

A assinatura deve ser gerada sobre a string `{x-api-nome}:{rota}`. Exemplo:

```
api_integrador_grupo_x:/lutas/
```

> **Importante:** a barra final `/` em `/lutas/` faz parte da rota. Para rotas com ID, assine exatamente a rota usada (ex: `/lutas/1`).

---

# 📥 Payload — Criar / Editar Luta

```json
{
  "data": "2026-07-20",
  "horario": "23:00",
  "id_lutador1": 1,
  "id_lutador2": 2
}
```

Regras:

- `id_lutador1` e `id_lutador2` devem ser **diferentes**
- Ambos os lutadores precisam existir na API externa de Lutadores
- Caso algum não exista, a API retorna erro `404`

---

# 🚀 Guia de Uso da API (GET, POST, PUT, DELETE)

## GET `/` — Status da API

Rota pública, sem autenticação.

**curl:**

```bash
curl https://betting-api-lutas.vercel.app/
```

**Resposta esperada:**

```json
{
  "status": "API de Lutas na Vercel",
  "docs": "/docs"
}
```

---

## GET `/lutas/` — Listar Lutas

Requer autenticação RSA.

**curl:**

```bash
curl -X GET https://betting-api-lutas.vercel.app/lutas/ \
  -H "x-api-nome: api_integrador_grupo_x" \
  -H "x-assinatura: <ASSINATURA_BASE64>"
```

**Python:**

```python
import os, requests

URL_LUTAS = os.getenv("URL_LUTAS", "https://betting-api-lutas.vercel.app")
rota = "/lutas/"

resposta = requests.get(
    f"{URL_LUTAS}{rota}",
    headers=headers_rsa(rota),
    timeout=8
)

print(resposta.status_code)
print(resposta.json())
```

**Resposta esperada (200):**

```json
[
  {
    "id": 1,
    "data": "2026-07-20",
    "horario": "23:00",
    "id_lutador1": 1,
    "id_lutador2": 2,
    "nome_lutador1": "McGregor",
    "nome_lutador2": "Poatan"
  }
]
```

---

## POST `/lutas/` — Criar uma Luta

Requer autenticação RSA.

**curl:**

```bash
curl -X POST https://betting-api-lutas.vercel.app/lutas/ \
  -H "Content-Type: application/json" \
  -H "x-api-nome: api_integrador_grupo_x" \
  -H "x-assinatura: <ASSINATURA_BASE64>" \
  -d '{
    "data": "2026-07-20",
    "horario": "23:00",
    "id_lutador1": 1,
    "id_lutador2": 2
  }'
```

**Python:**

```python
import os, requests

URL_LUTAS = os.getenv("URL_LUTAS", "https://betting-api-lutas.vercel.app")
rota = "/lutas/"

payload = {
    "data": "2026-07-20",
    "horario": "23:00",
    "id_lutador1": 1,
    "id_lutador2": 2
}

resposta = requests.post(
    f"{URL_LUTAS}{rota}",
    json=payload,
    headers=headers_rsa(rota),
    timeout=8
)

print(resposta.status_code)
print(resposta.json())
```

**Resposta esperada (200):**

```json
{
  "id": 1,
  "data": "2026-07-20",
  "horario": "23:00",
  "id_lutador1": 1,
  "id_lutador2": 2
}
```

**Evento RabbitMQ publicado:** `luta_criada`

---

## PUT `/lutas/{id}` — Editar uma Luta

Requer autenticação RSA. A rota assinada deve incluir o ID (ex: `/lutas/1`).

**curl:**

```bash
curl -X PUT https://betting-api-lutas.vercel.app/lutas/1 \
  -H "Content-Type: application/json" \
  -H "x-api-nome: api_integrador_grupo_x" \
  -H "x-assinatura: <ASSINATURA_BASE64>" \
  -d '{
    "data": "2026-07-21",
    "horario": "21:30",
    "id_lutador1": 1,
    "id_lutador2": 3
  }'
```

**Python:**

```python
import os, requests

URL_LUTAS = os.getenv("URL_LUTAS", "https://betting-api-lutas.vercel.app")

luta_id = 1
rota = f"/lutas/{luta_id}"

payload = {
    "data": "2026-07-21",
    "horario": "21:30",
    "id_lutador1": 1,
    "id_lutador2": 3
}

resposta = requests.put(
    f"{URL_LUTAS}{rota}",
    json=payload,
    headers=headers_rsa(rota),
    timeout=8
)

print(resposta.status_code)
print(resposta.json())
```

**Resposta esperada (200):**

```json
{
  "msg": "Luta atualizada com sucesso",
  "luta": {
    "id": 1,
    "data": "2026-07-21",
    "horario": "21:30",
    "id_lutador1": 1,
    "id_lutador2": 3
  }
}
```

**Evento RabbitMQ publicado:** `luta_editada`

---

## DELETE `/lutas/{id}` — Cancelar uma Luta

Requer autenticação RSA. A rota assinada deve incluir o ID (ex: `/lutas/1`).

**curl:**

```bash
curl -X DELETE https://betting-api-lutas.vercel.app/lutas/1 \
  -H "x-api-nome: api_integrador_grupo_x" \
  -H "x-assinatura: <ASSINATURA_BASE64>"
```

**Python:**

```python
import os, requests

URL_LUTAS = os.getenv("URL_LUTAS", "https://betting-api-lutas.vercel.app")

luta_id = 1
rota = f"/lutas/{luta_id}"

resposta = requests.delete(
    f"{URL_LUTAS}{rota}",
    headers=headers_rsa(rota),
    timeout=8
)

print(resposta.status_code)
print(resposta.json())
```

**Resposta esperada (200):**

```json
{
  "message": "Luta 1 cancelada com sucesso"
}
```

**Evento RabbitMQ publicado:** `luta_cancelada`

---

## POST `/admin/cadastrar-integrador` — Cadastrar Integrador

Rota administrativa protegida pelo header `X-Admin-Token`.

**curl:**

```bash
curl -X POST "https://betting-api-lutas.vercel.app/admin/cadastrar-integrador?nome_api=api_integrador_grupo_x&chave_publica=-----BEGIN%20PUBLIC%20KEY-----%0A...%0A-----END%20PUBLIC%20KEY-----" \
  -H "X-Admin-Token: <TOKEN_ADMIN>"
```

**Resposta esperada (200):**

```json
{
  "msg": "O grupo api_integrador_grupo_x foi autorizado com sucesso!"
}
```

---

# ⚠️ Códigos HTTP de Resposta

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | IDs dos lutadores são iguais |
| 401 | Headers de autenticação ausentes |
| 403 | Assinatura inválida ou token admin inválido |
| 404 | Luta ou lutador não encontrado |
| 422 | Payload JSON inválido |
| 500 | Erro interno do servidor |

---

# ⚠️ ATENÇÃO

A API de Lutas mantém dependência explícita da API de Lutadores (https://api-lutadoressd.onrender.com) para garantir consistência referencial distribuída. Como os lutadores são uma entidade externa ao domínio de lutas, a API valida os IDs antes de persistir o confronto. Caso integradores utilizem outras fontes de lutadores, o mapeamento entre IDs deve ser feito no próprio integrador, mantendo a API de Lutas desacoplada de múltiplos formatos externos.

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

# Instalação Online

Para implementação siga os arquivos Integração...md.

Para conexão forneça os dados requisitados para os administradores.

---

# Instalação Local

## 1. Clonar repositório

```bash
git clone https://github.com/DieegoVieira/betting_api.git
```

---

## 2. Entrar na pasta

```bash
cd betting_api
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