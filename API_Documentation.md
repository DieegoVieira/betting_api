# 📄 Documentação da API de Distribuição de Lutas

Esta API é responsável pelo agendamento e distribuição de lutas. Ela funciona como um microserviço restrito (backend isolado) que valida dados em um serviço externo de lutadores e exige autenticação entre servidores (M2M).

---

## 🌐 URL Base do Serviço

- **Local**: `http://127.0.0.1:8001` 
- **Público**: `https://betting-api-hmup.onrender.com` 

---

## 🛡️ Autenticação e Segurança (RSA)

A API **não possui acesso público aberto**. Todas as rotas de manipulação e consulta de dados estão protegidas pelo middleware `validar_api_externa`.

Para que uma requisição seja aceita, ela deve obrigatoriamente incluir os seguintes cabeçalhos (Headers):

- `x-api-nome`: Identificador de quem está chamando (ex: `api_integrador`).
- `x-assinatura`: Assinatura digital (em Base64) gerada com a **Chave Privada** do emissor. A API validará esta assinatura usando a sua **Chave Pública** cadastrada.

*A mensagem base para a assinatura deve ser o padrão:* `{x-api-nome}:{rota}`.

---

## 📌 Endpoints da API

| Método HTTP | Rota        | Proteção | Descrição |
|------------|------------|----------|----------|
| GET        | `/`          | N/A      | Verifica o status da API. |
| POST       | `/lutas/`    | 🔐 RSA     | Agenda uma nova luta (valida IDs na API externa). |
| GET        | `/lutas/`    | 🔐 RSA     | Lista todas as lutas agendadas (com nomes dos lutadores). |
| GET        | `/lutas/{id}`| 🔐 RSA     | Obtém detalhes de uma luta específica por ID. |
| DELETE     | `/lutas/{id}`| 🔐 RSA     | Cancela uma luta agendada e remove do banco. |

---

## ⛓️ Integração Distribuída

A API realiza chamadas síncronas para o serviço de lutadores hospedado em:

👉 `https://api-lutadoressd.onrender.com/api/lutadores/` 

O agendamento só é confirmado se ambos os lutadores retornarem **status 200 OK** na API externa. Durante a listagem (`GET /lutas/`), a API também consulta esse serviço para enriquecer os dados trocando IDs por apelidos.

---

## 📥 Estrutura de Dados para Agendamento (`POST /lutas/`)

Para agendar uma luta, envie um JSON com os campos obrigatórios no Corpo (Body) e os cabeçalhos de segurança:

```json
{
  "data": "2026-07-20",
  "horario": "23:00",
  "id_lutador1": 1,
  "id_lutador2": 2
}