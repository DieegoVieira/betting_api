# Guia de Integração com a API de Lutas

Este documento explica como integrar um sistema externo, incluindo aplicações em Node.js/TypeScript, com a API de Lutas.

A API de Lutas utiliza autenticação entre sistemas baseada em assinatura digital RSA. Portanto, antes de consumir as rotas protegidas, o integrador precisa ser cadastrado pela equipe responsável pela API de Lutas.

---

# ⚠️ ATENÇÃO

A API de Lutas mantém dependência explícita da API de Lutadores (https://api-lutadoressd.onrender.com) para garantir consistência referencial distribuída. Como os lutadores são uma entidade externa ao domínio de lutas, a API valida os IDs antes de persistir o confronto. Caso integradores utilizem outras fontes de lutadores, o mapeamento entre IDs deve ser feito no próprio integrador, mantendo a API de Lutas desacoplada de múltiplos formatos externos.

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

A assinatura deve ser gerada sobre a seguinte string:

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

# 3. O que o integrador precisa enviar para cadastro

Para ser autorizado, o integrador deve enviar para a equipe da API de Lutas:

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

Importante: envie apenas a chave pública. Nunca envie a chave privada.

---

# 4. Geração das chaves RSA em Node.js/TypeScript

Crie um arquivo chamado:

```text
generate-keys.ts
```

Com este conteúdo:

```ts
import { generateKeyPairSync } from "crypto";
import { writeFileSync } from "fs";

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
```

Execute:

```bash
npx ts-node generate-keys.ts
```

Serão gerados:

```text
private_key.pem
public_key.pem
```

O arquivo `public_key.pem` deve ser enviado para a equipe da API de Lutas.

O arquivo `private_key.pem` deve permanecer somente no integrador.

---

# 5. Instalar dependências

No projeto Node/TypeScript:

```bash
npm install axios
```

Se for usar TypeScript diretamente:

```bash
npm install -D ts-node typescript @types/node
```

---

# 6. Código base para assinar requisições

Crie um arquivo chamado:

```text
lutas-client.ts
```

Com este conteúdo:

```ts
import axios from "axios";
import { readFileSync } from "fs";
import { constants, sign } from "crypto";

const URL_LUTAS = process.env.URL_LUTAS || "https://betting-api-beta.vercel.app";
const NOME_INTEGRADOR = process.env.NOME_INTEGRADOR || "api_integrador_node";

function carregarChavePrivada(): string {
  if (process.env.PRIVATE_KEY_PEM) {
    return process.env.PRIVATE_KEY_PEM.replace(/\\n/g, "\n");
  }

  return readFileSync("private_key.pem", "utf8");
}

function gerarAssinatura(rota: string): string {
  const privateKey = carregarChavePrivada();

  const mensagem = `${NOME_INTEGRADOR}:${rota}`;

  const assinatura = sign("sha256", Buffer.from(mensagem), {
    key: privateKey,
    padding: constants.RSA_PKCS1_PSS_PADDING,
    saltLength: constants.RSA_PSS_SALTLEN_MAX_SIGN,
  });

  return assinatura.toString("base64");
}

function headersRSA(rota: string) {
  return {
    "x-api-nome": NOME_INTEGRADOR,
    "x-assinatura": gerarAssinatura(rota),
  };
}
```

---

# 7. Listar lutas

```ts
async function listarLutas() {
  const rota = "/lutas/";

  const resposta = await axios.get(`${URL_LUTAS}${rota}`, {
    headers: headersRSA(rota),
  });

  console.log(resposta.data);
}

listarLutas().catch((erro) => {
  if (erro.response) {
    console.error("Status:", erro.response.status);
    console.error("Erro:", erro.response.data);
  } else {
    console.error("Erro:", erro.message);
  }
});
```

---

# 8. Criar luta

```ts
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

criarLuta().catch((erro) => {
  if (erro.response) {
    console.error("Status:", erro.response.status);
    console.error("Erro:", erro.response.data);
  } else {
    console.error("Erro:", erro.message);
  }
});
```

---

# 9. Editar luta

```ts
async function editarLuta(id: number) {
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

editarLuta(1).catch((erro) => {
  if (erro.response) {
    console.error("Status:", erro.response.status);
    console.error("Erro:", erro.response.data);
  } else {
    console.error("Erro:", erro.message);
  }
});
```

---

# 10. Cancelar luta

```ts
async function deletarLuta(id: number) {
  const rota = `/lutas/${id}`;

  const resposta = await axios.delete(`${URL_LUTAS}${rota}`, {
    headers: headersRSA(rota),
  });

  console.log(resposta.data);
}

deletarLuta(1).catch((erro) => {
  if (erro.response) {
    console.error("Status:", erro.response.status);
    console.error("Erro:", erro.response.data);
  } else {
    console.error("Erro:", erro.message);
  }
});
```

---

# 11. Variáveis de ambiente recomendadas

Em ambiente online, como Vercel, Render ou Railway, configure:

```env
URL_LUTAS=https://betting-api-beta.vercel.app
NOME_INTEGRADOR=api_integrador_node
PRIVATE_KEY_PEM=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----
```

Não suba `private_key.pem` para o GitHub.

Adicione no `.gitignore`:

```gitignore
private_key.pem
.env
node_modules/
dist/
```

---

# 12. Atenção à rota assinada

A rota assinada precisa ser exatamente igual à rota chamada.

Para listar ou criar lutas:

```text
/lutas/
```

Mensagem assinada:

```text
api_integrador_node:/lutas/
```

Para editar ou deletar a luta de ID 5:

```text
/lutas/5
```

Mensagem assinada:

```text
api_integrador_node:/lutas/5
```

Se assinar `/lutas` e chamar `/lutas/`, a assinatura será inválida.

---

# 13. Endpoints disponíveis

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Verifica status da API |
| GET | `/lutas/` | Lista todas as lutas |
| POST | `/lutas/` | Cria uma nova luta |
| PUT | `/lutas/{id}` | Edita uma luta |
| DELETE | `/lutas/{id}` | Cancela uma luta |

---

# 14. Payload para criar/editar luta

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
- caso a API de Lutadores esteja indisponível, criação e edição podem falhar;
- a listagem de lutas pode retornar `Lutador indisponível (ID X)` em caso de falha externa.

---

# 15. Erros comuns

| Código | Causa provável |
|---|---|
| 401 | Headers `x-api-nome` ou `x-assinatura` ausentes |
| 403 | Assinatura inválida ou integrador não cadastrado |
| 404 | Luta ou lutador não encontrado |
| 422 | Payload inválido |
| 500 | Erro interno da API |

---

# 16. Checklist final

Antes de testar, confirme:

- o integrador gerou as chaves RSA;
- a chave pública foi enviada para cadastro;
- o `nome_api` usado no código é igual ao cadastrado;
- a chave privada corresponde à chave pública enviada;
- a rota assinada é exatamente igual à rota chamada;
- a URL base da API está correta;
- o header `x-api-nome` está sendo enviado;
- o header `x-assinatura` está sendo enviado.

```text
URL correta:
https://betting-api-beta.vercel.app

Docs:
https://betting-api-beta.vercel.app/docs
```