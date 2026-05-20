# 📄 Documentação Técnica — Microserviço de Lutas

Esta API é o componente central de agendamento do ecossistema distribuído.

Ela implementa:

- Comunicação distribuída
- Segurança M2M
- RabbitMQ
- Arquitetura orientada a eventos
- Interoperabilidade entre microsserviços

---

# 🌐 Endpoints de Acesso

## 🚀 Produção

```bash
https://betting-api-lutas.vercel.app
```

---

## 📚 Swagger

```bash
https://betting-api-lutas.vercel.app/docs
```

---

# 🛡️ Segurança RSA-PSS

As rotas protegidas utilizam autenticação M2M baseada em assinatura digital RSA.

---

# 🔐 Headers Obrigatórios

```http
x-api-nome
x-assinatura
```

---

# 📌 Descrição dos Headers

| Header | Descrição |
|---|---|
| x-api-nome | Nome do integrador |
| x-assinatura | Assinatura RSA em Base64 |

---

# 🧠 Lógica da Assinatura

A assinatura deve ser gerada sobre:

```text
{x-api-nome}:{rota}
```

---

## Exemplo

```text
api_integrador:/lutas/
```

---

# 🔒 Algoritmos Utilizados

- RSA
- SHA256
- Padding PSS

---

# 📌 Endpoints

| Método | Rota | Proteção | Descrição |
|---|---|---|---|
| GET | / | N/A | Status da API |
| POST | /admin/cadastrar-integrador | X-Admin-Token | Cadastro de integrador |
| GET | /lutas/ | RSA | Lista lutas |
| POST | /lutas/ | RSA | Cria luta |
| PUT | /lutas/{id} | RSA | Edita luta |
| DELETE | /lutas/{id} | RSA | Remove luta |

---

# 📥 Payload — Criar/Editar Luta

```json
{
  "data": "2026-07-20",
  "horario": "23:00",
  "id_lutador1": 1,
  "id_lutador2": 2
}
```

---

# 📥 Payload — Cadastro de Integrador

| Campo | Descrição |
|---|---|
| nome_api | Nome do integrador |
| chave_publica | Chave pública RSA PEM |

---

# ⛓️ Fluxo Distribuído

## 1️⃣ Validação RSA

A assinatura é validada utilizando a chave pública armazenada no PostgreSQL.

Objetivos:

- autenticidade
- integridade
- origem confiável

---

## 2️⃣ Consulta Distribuída

A API consulta o microserviço externo:

```bash
https://api-lutadoressd.onrender.com/api/lutadores/{id}
```

Objetivos:

- validar existência
- manter consistência distribuída

---

## 3️⃣ Persistência

Após validações:

- dados persistidos no PostgreSQL
- evento publicado no RabbitMQ

---

## 4️⃣ Enriquecimento Distribuído

Ao listar lutas:

- IDs são convertidos em apelidos
- API consulta o microserviço externo

---

# 🐇 RabbitMQ — Comunicação Assíncrona

A API publica eventos distribuídos utilizando RabbitMQ.

---

# 📌 Fila

```text
eventos_lutas
```

---

# 📤 Eventos Publicados

| Evento | Descrição |
|---|---|
| luta_criada | Nova luta cadastrada |
| luta_editada | Luta atualizada |
| luta_cancelada | Luta removida |

---

# 📦 Exemplo de Evento

```json
{
  "evento": "luta_criada",
  "dados": {
    "id": 1,
    "data": "2026-07-20",
    "horario": "23:00",
    "id_lutador1": 1,
    "id_lutador2": 2
  }
}
```

---

# 🎯 Objetivos da Mensageria

- Desacoplamento
- Comunicação assíncrona
- Integração futura
- Tolerância parcial a falhas
- Arquitetura orientada a eventos

---

# ⚠️ Tratamento de Falhas Distribuídas

Se um lutador for removido:

```text
Lutador removido (ID X)
```

Se a API externa estiver indisponível:

```text
Lutador indisponível (ID X)
```

---

# ⚠️ Códigos HTTP

| Código | Descrição |
|---|---|
| 200 | Sucesso |
| 401 | Headers ausentes |
| 403 | Assinatura inválida |
| 404 | Luta/lutador não encontrado |
| 422 | JSON inválido |
| 500 | Erro interno |

---

# 🧠 Conceitos de Sistemas Distribuídos

- REST
- Microsserviços
- RabbitMQ
- AMQP
- Comunicação síncrona
- Comunicação assíncrona
- Event-Driven Architecture
- Segurança distribuída
- RSA
- JWT
- Persistência distribuída
- Cloud Computing
- Serverless
- Zero Trust Security

---

# 👨‍💻 Autores

Projeto desenvolvido para Sistemas Distribuídos.

- João Pedro Silva da Rosa Lima
- Armando Alves de Oliveira Braga
- Sophia Ishii Dognani

---

# 👨‍💻 Autores

Sistema desenvolvido para a disciplina de Sistemas Distribuídos.

* João Pedro Silva da Rosa Lima
* Armando Alves de Oliveira Braga
* Sophia Ishii Dognani