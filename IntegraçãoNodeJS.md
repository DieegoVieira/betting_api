# Guia de Integração com a API de Lutas — Node.js JavaScript

Este documento explica como integrar uma aplicação Node.js com a API de Lutas utilizando autenticação M2M baseada em assinatura digital RSA.

A API de Lutas exige que o integrador seja previamente cadastrado pela equipe responsável pela API.

---

# 1. URL da API

URL de produção:

```text
https://betting-api-beta.vercel.app
```

Swagger:

```text
https://betting-api-beta.vercel.app/docs
```

---

# 2. Modelo de autenticação

Todas as rotas protegidas exigem dois headers:

```http
x-api-nome: nome_do_integrador
x-assinatura: assinatura_rsa_base64
```

A assinatura deve ser gerada sobre a string:

```text
{x-api-nome}:{rota}
```

Exemplo:

```text
api_integrador_node:/lutas/
```

A assinatura deve usar:

```text
RSA-PSS + SHA256 + Base64
```

---

# 3. O que enviar para cadastro

O integrador deve enviar para a equipe da API de Lutas:

```text
Nome da API integradora:
URL do integrador:
Chave pública RSA:
Responsável técnico:
```

Exemplo:

```text
Nome da API integradora: api_integrador_node
URL do integrador: https://meu-integrador.vercel.app
Responsável técnico: Nome do aluno
Chave pública RSA:
-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----
```

Envie somente a chave pública.  
Nunca envie a chave privada.

---

# 4. Criar projeto Node.js

```bash
mkdir integrador-lutas-node
cd integrador-lutas-node
npm init -y
```

Instale o Axios:

```bash
npm install axios
```

---

# 5. Gerar chaves RSA em JavaScript

Crie um arquivo:

```text
generate-keys.js
```

Com este conteúdo:

```js
const { generateKeyPairSync } = require("crypto");
const { writeFileSync } = require("fs");

const { publicKey, privateKey } = generateKeyPairSync("rsa", {
  modulusLength: 2048,
  publicKeyEncoding: {
    type: "spki",
    format: "pem",
  },
  privateKeyEncoding: {
    type: "pkcs8",
    format: "pem",
  },
});

writeFileSync("private_key.pem", privateKey);
writeFileSync("public_key.pem", publicKey);

console.log("Chaves RSA geradas com sucesso.");
console.log("Envie o arquivo public_key.pem para a equipe da API de Lutas.");
console.log("Nunca compartilhe o arquivo private_key.pem.");
```

Execute:

```bash
node generate-keys.js
```

Serão gerados:

```text
private_key.pem
public_key.pem
```

O `public_key.pem` deve ser enviado para cadastro.  
O `private_key.pem` deve ficar somente no projeto do integrador.

---

# 6. Cliente Node.js para consumir a API

Crie um arquivo:

```text
lutas-client.js
```

Com este conteúdo:

```js
const axios = require("axios");
const fs = require("fs");
const crypto = require("crypto");

const URL_LUTAS = process.env.URL_LUTAS || "https://betting-api-beta.vercel.app";
const NOME_INTEGRADOR = process.env.NOME_INTEGRADOR || "api_integrador_node";

function carregarChavePrivada() {
  if (process.env.PRIVATE_KEY_PEM) {
    return process.env.PRIVATE_KEY_PEM.replace(/\\n/g, "\n");
  }

  return fs.readFileSync("private_key.pem", "utf8");
}

function gerarAssinatura(rota) {
  const privateKey = carregarChavePrivada();

  const mensagem = `${NOME_INTEGRADOR}:${rota}`;

  const assinatura = crypto.sign("sha256", Buffer.from(mensagem), {
    key: privateKey,
    padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
    saltLength: crypto.constants.RSA_PSS_SALTLEN_MAX_SIGN,
  });

  return assinatura.toString("base64");
}

function headersRSA(rota) {
  return {
    "x-api-nome": NOME_INTEGRADOR,
    "x-assinatura": gerarAssinatura(rota),
  };
}

async function listarLutas() {
  const rota = "/lutas/";

  const resposta = await axios.get(`${URL_LUTAS}${rota}`, {
    headers: headersRSA(rota),
  });

  console.log(resposta.data);
}

async function criarLuta() {
  const rota = "/lutas/";

  const payload = {
    data: "2026-07-20",
    horario: "23:00",
    id_lutador1: 1,
    id_lutador2: 2,
  };

  const resposta = await axios.post(`${URL_LUTAS}${rota}`, payload, {
    headers: headersRSA(rota),
  });

  console.log(resposta.data);
}

async function editarLuta(id) {
  const rota = `/lutas/${id}`;

  const payload = {
    data: "2026-07-21",
    horario: "21:30",
    id_lutador1: 1,
    id_lutador2: 3,
  };

  const resposta = await axios.put(`${URL_LUTAS}${rota}`, payload, {
    headers: headersRSA(rota),
  });

  console.log(resposta.data);
}

async function deletarLuta(id) {
  const rota = `/lutas/${id}`;

  const resposta = await axios.delete(`${URL_LUTAS}${rota}`, {
    headers: headersRSA(rota),
  });

  console.log(resposta.data);
}

async function executar() {
  try {
    await listarLutas();

    // Descomente para testar:
    // await criarLuta();
    // await editarLuta(1);
    // await deletarLuta(1);

  } catch (erro) {
    if (erro.response) {
      console.error("Status:", erro.response.status);
      console.error("Erro:", erro.response.data);
    } else {
      console.error("Erro:", erro.message);
    }
  }
}

executar();
```

---

# 7. Rodar o teste

Após enviar sua chave pública e ser cadastrado pela equipe da API de Lutas, execute:

```bash
node lutas-client.js
```

Se tudo estiver correto, a listagem de lutas será exibida no terminal.

---

# 8. Exemplo separado: listar lutas

```js
async function listarLutas() {
  const rota = "/lutas/";

  const resposta = await axios.get(`${URL_LUTAS}${rota}`, {
    headers: headersRSA(rota),
  });

  return resposta.data;
}
```

---

# 9. Exemplo separado: criar luta

```js
async function criarLuta() {
  const rota = "/lutas/";

  const payload = {
    data: "2026-07-20",
    horario: "23:00",
    id_lutador1: 1,
    id_lutador2: 2,
  };

  const resposta = await axios.post(`${URL_LUTAS}${rota}`, payload, {
    headers: headersRSA(rota),
  });

  return resposta.data;
}
```

---

# 10. Exemplo separado: editar luta

```js
async function editarLuta(id) {
  const rota = `/lutas/${id}`;

  const payload = {
    data: "2026-07-21",
    horario: "21:30",
    id_lutador1: 1,
    id_lutador2: 3,
  };

  const resposta = await axios.put(`${URL_LUTAS}${rota}`, payload, {
    headers: headersRSA(rota),
  });

  return resposta.data;
}
```

---

# 11. Exemplo separado: deletar luta

```js
async function deletarLuta(id) {
  const rota = `/lutas/${id}`;

  const resposta = await axios.delete(`${URL_LUTAS}${rota}`, {
    headers: headersRSA(rota),
  });

  return resposta.data;
}
```

---

# 12. Variáveis de ambiente

Em produção, como Vercel, Render ou Railway, configure:

```env
URL_LUTAS=https://betting-api-beta.vercel.app
NOME_INTEGRADOR=api_integrador_node
PRIVATE_KEY_PEM=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----
```

O `NOME_INTEGRADOR` deve ser exatamente igual ao nome cadastrado na API de Lutas.

---

# 13. `.gitignore`

Não suba chaves privadas nem dependências:

```gitignore
node_modules/
.env
private_key.pem
```

O arquivo `public_key.pem` pode ser compartilhado com a equipe da API de Lutas, mas não precisa ser público no GitHub.

---

# 14. Atenção à rota assinada

A rota assinada precisa ser exatamente igual à rota chamada.

Para listar ou criar:

```text
/lutas/
```

Mensagem assinada:

```text
api_integrador_node:/lutas/
```

Para editar ou deletar luta de ID 5:

```text
/lutas/5
```

Mensagem assinada:

```text
api_integrador_node:/lutas/5
```

Se a rota assinada for diferente da rota chamada, a API retornará:

```json
{
  "detail": "Assinatura inválida"
}
```

---

# 15. Endpoints disponíveis

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Verifica status da API |
| GET | `/lutas/` | Lista todas as lutas |
| POST | `/lutas/` | Cria uma nova luta |
| PUT | `/lutas/{id}` | Edita uma luta |
| DELETE | `/lutas/{id}` | Cancela uma luta |

---

# 16. Payload para criar/editar luta

```json
{
  "data": "2026-07-20",
  "horario": "23:00",
  "id_lutador1": 1,
  "id_lutador2": 2
}
```

Regras:

- `id_lutador1` e `id_lutador2` devem ser diferentes;
- os lutadores precisam existir na API de Lutadores;
- caso a API de Lutadores esteja indisponível, criação e edição podem falhar.

---

# 17. Erros comuns

| Código | Causa provável |
|---|---|
| 401 | Headers `x-api-nome` ou `x-assinatura` ausentes |
| 403 | Assinatura inválida ou integrador não cadastrado |
| 404 | Luta ou lutador não encontrado |
| 422 | Payload inválido |
| 500 | Erro interno da API |

---

# 18. Checklist final

Antes de testar, confirme:

- gerou `private_key.pem` e `public_key.pem`;
- enviou `public_key.pem` para cadastro;
- não compartilhou `private_key.pem`;
- o `NOME_INTEGRADOR` é igual ao cadastrado;
- a rota assinada é exatamente igual à rota chamada;
- a URL da API está correta;
- os headers `x-api-nome` e `x-assinatura` estão sendo enviados.

```text
URL:
https://betting-api-beta.vercel.app

Docs:
https://betting-api-beta.vercel.app/docs
```