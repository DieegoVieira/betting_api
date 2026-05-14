# 🥊 API de Apostas em Lutas - Sistemas Distribuídos (Microserviço)

Este projeto consiste em uma API RESTful desenvolvida para simular um sistema de agendamento e gestão de lutas. Ele foi construído como parte da disciplina de Sistemas Distribuídos, demonstrando a interoperabilidade entre serviços independentes e implementando uma **Arquitetura de Segurança M2M (Machine-to-Machine) com Criptografia Assimétrica RSA**.

> ⚠️ **Nota de Arquitetura:**  
> Este repositório contém o **Microserviço de Backend (API de Lutas)**.  
> A interface web e o Gateway de autenticação de usuários residem em um repositório separado (**Integrador**).

---

# 🌐 URL de Acesso (Produção)

A API está hospedada e pronta para receber requisições em:

👉 `https://betting-api-lutas.vercel.app`

> *(Nota: Requisições diretas via navegador retornarão Erro 401/403 devido à exigência de assinatura digital nos cabeçalhos).*

---

# 🚀 Tecnologias Utilizadas

- **Python 3.11+** — Linguagem de programação principal.
- **FastAPI** — Framework de alta performance para construção de APIs.
- **Cryptography** — Validação de assinaturas digitais RSA (*Zero Trust Security*).
- **SQLAlchemy** — ORM para abstração e persistência de dados.
- **PostgreSQL (Neon.tech)** — Banco de dados relacional em nuvem para persistência real.
- **Vercel** — Plataforma de hospedagem Serverless.

---

# 📁 Estrutura do Projeto

```bash
betting_api/
├── API_lutas.py         # Orquestrador da API e definição de rotas
├── models.py            # Definição das tabelas (Lutas e Integradores)
├── security.py          # Motor de validação criptográfica RSA
├── acess_log.py         # Auditoria e logs de requisições (capturados pela Vercel)
├── vercel.json          # Configuração de deploy Serverless
├── requirements.txt     # Dependências do projeto
└── API_Documentation.md # Documentação técnica dos endpoints
````

---

# 🛡️ Segurança M2M (Machine-to-Machine)

Para garantir que apenas sistemas autorizados possam gerenciar o calendário de lutas, a API utiliza **Assinatura Digital RSA**.

---

# 🔐 Fluxo de Validação

## 1️⃣ Recepção da Requisição

A API intercepta os cabeçalhos:

```http
X-API-Nome
X-Assinatura
```

---

## 2️⃣ Identificação do Integrador

O sistema consulta o banco de dados em busca da **Chave Pública** vinculada ao integrador informado.

---

## 3️⃣ Validação Criptográfica

O motor de segurança utiliza a chave pública armazenada para validar matematicamente a assinatura enviada.

A autenticação garante:

* Integridade da mensagem
* Autenticidade do integrador
* Segurança sem compartilhamento de segredos

---

## 4️⃣ Interoperabilidade com Microsserviços

Após a validação RSA, a API realiza uma consulta ao microserviço externo de lutadores:

```bash
https://api-lutadoressd.onrender.com/api/lutadores/
```

Objetivo:

* Confirmar existência dos atletas
* Garantir consistência dos dados distribuídos

---

## 5️⃣ Persistência

A luta somente é registrada no banco de dados se:

* A assinatura RSA for válida
* O integrador estiver autorizado
* Os lutadores existirem

---

# ⚙️ Execução Local

# 1️⃣ Instalação

```bash
git clone https://github.com/joaofoguin/betting_api
cd betting_api

pip install -r requirements.txt
```

---

# 2️⃣ Variáveis de Ambiente

Crie um arquivo `.env` ou configure as variáveis diretamente no terminal.

## DATABASE_URL

String de conexão do banco de dados.

Exemplos:

```env
DATABASE_URL=postgresql://usuario:senha@host/database
```

ou

```env
DATABASE_URL=sqlite:///./local.db
```

---

## SENHA_ADMIN

Token utilizado para cadastro de novos integradores via Swagger/Admin API.

Exemplo:

```env
SENHA_ADMIN=minha_senha_segura
```

---

# 3️⃣ Iniciar Servidor

```bash
uvicorn API_lutas:app --reload
```

A API será iniciada localmente.

---

# ☁️ Deploy na Vercel

O projeto está otimizado para ambiente **Serverless** da Vercel.

---

## 💾 Persistência

Utiliza:

* **PostgreSQL**
* **Neon.tech**
* Conexão persistente em nuvem

---

## 📜 Logs e Auditoria

O sistema utiliza:

```python
print()
```

Os logs são automaticamente capturados pelo painel da Vercel.

Isso permite:

* Auditoria
* Monitoramento
* Rastreamento de acessos
* Diagnóstico de falhas

---

## ⚙️ Configuração

O arquivo:

```bash
vercel.json
```

define:

* Runtime Python
* Mapeamento de rotas
* Estratégia Serverless

---

# 📚 Documentação Interativa

A documentação Swagger está disponível em:

👉 `https://betting-api-lutas.vercel.app/docs`

---

## 💡 Cadastro de Integradores

Para cadastrar um novo integrador, utilize:

```bash
/admin/cadastrar-integrador
```

Enviando no cabeçalho:

```http
X-Admin-Token
```

com o valor definido em:

```env
SENHA_ADMIN
```

---

# 🧠 Conceitos de Sistemas Distribuídos Aplicados

Este projeto implementa diversos conceitos fundamentais da disciplina:

* Comunicação síncrona entre microserviços
* APIs RESTful
* Interoperabilidade entre serviços
* Segurança distribuída
* Autenticação M2M
* Criptografia assimétrica RSA
* Persistência relacional em nuvem
* Arquitetura Serverless
* Auditoria distribuída
* Rastreabilidade de acessos
* Validação de integridade
* Integração HTTP/REST

---

# 👨‍💻 Autores

* João Pedro Silva da Rosa Lima
* Armando Alves de Oliveira Braga
* Sophia Ishii Dognani