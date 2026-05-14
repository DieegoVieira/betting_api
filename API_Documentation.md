# 📄 Documentação Técnica — Microserviço de Lutas

Esta API é o componente central de agendamento do ecossistema distribuído.  
Ela funciona como um microserviço restrito que implementa:

- Interoperabilidade entre serviços
- Comunicação distribuída
- Segurança M2M via Assinaturas Digitais RSA

---

# 🌐 Endpoints de Acesso

## 🚀 Produção (Vercel)

```bash
https://betting-api-lutas.vercel.app
````

---

## 📚 Documentação Viva (Swagger)

```bash
/docs
```

Exemplo:

```bash
https://betting-api-lutas.vercel.app/docs
```

---

# 🛡️ Protocolo de Segurança (RSA-PSS)

O acesso às rotas de dados é restrito.

O middleware de segurança exige:

* Validação de origem
* Integridade da requisição
* Autenticação M2M

---

# 🔐 Cabeçalhos Obrigatórios (Headers)

Todas as rotas protegidas exigem:

```http
x-api-nome
x-assinatura
```

---

## 📌 Descrição dos Headers

| Header         | Descrição                         |
| -------------- | --------------------------------- |
| `x-api-nome`   | Identificador único do integrador |
| `x-assinatura` | Assinatura digital RSA em Base64  |

---

# 🧠 Lógica da Assinatura

A assinatura deve ser gerada utilizando a seguinte string:

```text
{x-api-nome}:{caminho_da_rota}
```

---

## ✅ Exemplo

```text
api_integrador:/lutas/
```

Essa string deve ser assinada utilizando:

* RSA
* Padding PSS
* SHA256

---

# 📌 Catálogo de Endpoints

| Método   | Rota                          | Proteção        | Descrição                       |
| -------- | ----------------------------- | --------------- | ------------------------------- |
| `GET`    | `/`                           | N/A             | Verifica se a API está online   |
| `POST`   | `/admin/cadastrar-integrador` | `X-Admin-Token` | Registra uma nova chave pública |
| `GET`    | `/lutas/`                     | 🔐 RSA          | Lista todos os agendamentos     |
| `POST`   | `/lutas/`                     | 🔐 RSA          | Cria um novo agendamento        |
| `PUT`    | `/lutas/{id}`                 | 🔐 RSA          | Edita uma luta existente        |
| `DELETE` | `/lutas/{id}`                 | 🔐 RSA          | Remove uma luta do banco        |

---

# 📥 Definição de Payloads

# 1️⃣ Agendamento / Edição de Luta

Utilizado nas rotas:

* `POST /lutas/`
* `PUT /lutas/{id}`

---

## Corpo da Requisição (JSON)

```json
{
  "data": "2026-07-20",
  "horario": "23:00",
  "id_lutador1": 1,
  "id_lutador2": 2
}
```

---

# 2️⃣ Cadastro de Integrador

Rota:

```http
POST /admin/cadastrar-integrador
```

---

## Parâmetros Esperados

| Campo           | Descrição                        |
| --------------- | -------------------------------- |
| `nome_api`      | Nome único do integrador         |
| `chave_publica` | Chave pública RSA em formato PEM |

---

# ⛓️ Fluxo de Interoperabilidade Distribuída

Ao receber uma solicitação de agendamento ou edição, a API executa um fluxo síncrono de validação.

---

## 1️⃣ Validação de Identidade

A assinatura RSA é validada utilizando a chave pública armazenada no banco de dados.

Objetivo:

* Garantir autenticidade
* Confirmar origem da requisição
* Evitar falsificação

---

## 2️⃣ Consulta Externa

A API realiza uma consulta HTTP no microserviço externo de lutadores:

```bash
https://api-lutadoressd.onrender.com/api/lutadores/{id}
```

Objetivo:

* Confirmar existência dos competidores
* Garantir consistência distribuída

---

## 3️⃣ Consolidação

Se todas as verificações forem aprovadas:

* Assinatura válida
* Integrador autorizado
* Lutadores existentes

então os dados são persistidos no PostgreSQL.

---

## 4️⃣ Enriquecimento de Dados

Ao listar lutas agendadas, a API consulta novamente o microserviço externo para substituir IDs numéricos pelos apelidos dos lutadores.

Isso melhora:

* Legibilidade
* Interoperabilidade
* Experiência do cliente consumidor

---

# ⚠️ Códigos de Resposta

| Código                     | Descrição                                        |
| -------------------------- | ------------------------------------------------ |
| `200 OK`                   | Operação realizada com sucesso                   |
| `401 Unauthorized`         | Cabeçalhos de segurança ausentes                 |
| `403 Forbidden`            | Assinatura RSA inválida ou Token Admin incorreto |
| `404 Not Found`            | Luta ou lutador não encontrado                   |
| `422 Unprocessable Entity` | JSON inválido ou erro de validação               |

---

# 🧠 Conceitos de Sistemas Distribuídos Aplicados

Este projeto implementa na prática:

* Comunicação síncrona HTTP/REST
* Segurança distribuída
* Assinatura digital RSA
* Interoperabilidade entre serviços
* Integração entre microserviços
* Persistência relacional
* Arquitetura distribuída
* Auditoria de acessos
* Enriquecimento distribuído de dados
* Autenticação M2M
* Zero Trust Security

---

# 👨‍💻 Autores

Sistema desenvolvido para a disciplina de Sistemas Distribuídos.

* João Pedro Silva da Rosa Lima
* Armando Alves de Oliveira Braga
* Sophia Ishii Dognani