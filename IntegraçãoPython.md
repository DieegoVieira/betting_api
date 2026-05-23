# Guia de Integração Online — API de Lutas

Este documento explica como outro grupo ou integrador pode consumir a API de Lutas de forma online, utilizando autenticação M2M baseada em assinatura digital RSA.

A API de Lutas possui rotas protegidas. Portanto, qualquer integrador externo precisa ser previamente cadastrado pelos administradores da API.

---

# ⚠️ ATENÇÃO

A API de Lutas mantém dependência explícita da API de Lutadores (https://api-lutadoressd.onrender.com) para garantir consistência referencial distribuída. Como os lutadores são uma entidade externa ao domínio de lutas, a API valida os IDs antes de persistir o confronto. Caso integradores utilizem outras fontes de lutadores, o mapeamento entre IDs deve ser feito no próprio integrador, mantendo a API de Lutas desacoplada de múltiplos formatos externos.

---

# 1. URL da API de Lutas

A API está disponível em produção em:

```bash
https://betting-api-beta.vercel.app
```

Documentação Swagger:

```bash
https://betting-api-beta.vercel.app/docs
```

---

# 2. Modelo de Segurança

A API utiliza autenticação entre serviços com:

- RSA
- SHA256
- Padding PSS
- Assinatura Base64
- Cadastro prévio de integradores autorizados

O integrador deve possuir:

- uma chave privada RSA
- uma chave pública RSA

A chave privada fica somente com o integrador.

A chave pública deve ser enviada aos administradores da API de Lutas para cadastro.

---

# 3. O que o integrador deve enviar para a equipe da API de Lutas

Para ser cadastrado, o integrador deve enviar:

```text
nome_api
chave_publica
```

Exemplo:

```text
nome_api: api_integrador_grupo_x
```

E a chave pública no formato PEM:

```pem
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
-----END PUBLIC KEY-----
```

A equipe da API de Lutas cadastrará esses dados no endpoint administrativo:

```http
POST /admin/cadastrar-integrador
```

Esse endpoint é restrito e só pode ser usado pelos administradores da API de Lutas.

---

# 4. O que o integrador deve configurar no próprio projeto

O integrador deve armazenar estas variáveis de ambiente no seu provedor online, como Vercel, Render, Railway ou outro:

```env
URL_LUTAS=https://betting-api-beta.vercel.app
NOME_INTEGRADOR=api_integrador_grupo_x
PRIVATE_KEY_PEM="-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_PRIVADA_AQUI\n-----END PRIVATE KEY-----"
```

Importante:

- nunca subir a chave privada para o GitHub;
- nunca compartilhar a chave privada;
- enviar somente a chave pública para cadastro.

---

# 5. Geração das chaves RSA

O integrador pode gerar as chaves com Python.

Crie um arquivo chamado:

```bash
gerar_chaves.py
```

Com o seguinte conteúdo:

```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()

with open("private_key.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

with open("public_key.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Chaves RSA geradas com sucesso.")
```

Execute:

```bash
python gerar_chaves.py
```

Serão gerados:

```text
private_key.pem
public_key.pem
```

O arquivo `public_key.pem` deve ser enviado para cadastro.

O arquivo `private_key.pem` deve permanecer somente no integrador.

---

# 6. Como gerar a assinatura no integrador

Todas as requisições protegidas devem enviar dois headers:

```http
x-api-nome
x-assinatura
```

A assinatura deve ser gerada sobre esta string:

```text
{x-api-nome}:{rota}
```

Exemplo:

```text
api_integrador_grupo_x:/lutas/
```

Código Python para gerar assinatura:

```python
import os
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


NOME_INTEGRADOR = os.getenv("NOME_INTEGRADOR", "api_integrador_grupo_x")


def carregar_chave_privada():
    private_key_env = os.getenv("PRIVATE_KEY_PEM")

    if private_key_env:
        private_key_env = private_key_env.replace("\\n", "\n")
        return serialization.load_pem_private_key(
            private_key_env.encode("utf-8"),
            password=None
        )

    with open("private_key.pem", "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def gerar_assinatura(rota: str):
    private_key = carregar_chave_privada()

    mensagem = f"{NOME_INTEGRADOR}:{rota}"

    assinatura = private_key.sign(
        mensagem.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return base64.b64encode(assinatura).decode("utf-8")


def headers_rsa(rota: str):
    return {
        "x-api-nome": NOME_INTEGRADOR,
        "x-assinatura": gerar_assinatura(rota)
    }
```

---

# 7. Exemplo de consumo da API de Lutas

## Listar lutas

```python
import os
import requests

URL_LUTAS = os.getenv("URL_LUTAS", "https://betting-api-beta.vercel.app")

rota = "/lutas/"

resposta = requests.get(
    f"{URL_LUTAS}{rota}",
    headers=headers_rsa(rota),
    timeout=8
)

print(resposta.status_code)
print(resposta.json())
```

---

## Criar uma luta

```python
import os
import requests

URL_LUTAS = os.getenv("URL_LUTAS", "https://betting-api-beta.vercel.app")

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

---

## Editar uma luta

```python
import os
import requests

URL_LUTAS = os.getenv("URL_LUTAS", "https://betting-api-beta.vercel.app")

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

---

## Cancelar uma luta

```python
import os
import requests

URL_LUTAS = os.getenv("URL_LUTAS", "https://betting-api-beta.vercel.app")

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

---

# 8. Endpoints disponíveis

| Método | Rota | Proteção | Descrição |
|---|---|---|---|
| GET | `/` | Pública | Verifica status da API |
| GET | `/lutas/` | RSA | Lista todas as lutas |
| POST | `/lutas/` | RSA | Cria uma nova luta |
| PUT | `/lutas/{id}` | RSA | Edita uma luta |
| DELETE | `/lutas/{id}` | RSA | Cancela uma luta |

---

# 9. Payload de criação/edição

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
- os dois lutadores precisam existir na API de Lutadores;
- caso algum lutador não exista, a API retorna erro `404`.

---

# 10. Códigos de erro comuns

| Código | Motivo |
|---|---|
| 401 | Headers de autenticação ausentes |
| 403 | Assinatura inválida ou integrador não autorizado |
| 404 | Luta ou lutador não encontrado |
| 422 | Payload inválido |
| 500 | Erro interno da API |

---

# 11. Checklist para integração

Antes de consumir a API de Lutas, o integrador deve:

- gerar par de chaves RSA;
- guardar a chave privada com segurança;
- enviar a chave pública para a equipe da API de Lutas;
- informar o `nome_api` desejado;
- aguardar o cadastro;
- configurar `NOME_INTEGRADOR`;
- configurar `PRIVATE_KEY_PEM`;
- configurar `URL_LUTAS`;
- assinar cada requisição usando a rota exata.

---

# 12. Atenção à rota exata

A assinatura depende da rota.

Para listar ou criar lutas, a rota correta é:

```text
/lutas/
```

Com barra final.

Portanto, a mensagem assinada deve ser:

```text
api_integrador_grupo_x:/lutas/
```

Para editar ou deletar uma luta, a rota deve incluir o ID:

```text
/lutas/1
```

Exemplo de mensagem assinada:

```text
api_integrador_grupo_x:/lutas/1
```

Se a rota assinada for diferente da rota chamada, a API retornará:

```json
{
  "detail": "Assinatura inválida"
}
```

---

# 13. Modelo de segurança adotado

A API de Lutas utiliza cadastro administrativo de integradores.

Isso significa que o integrador não se cadastra livremente.

Fluxo correto:

```text
1. Integrador gera chave pública e privada
2. Integrador envia nome_api e chave pública para os administradores
3. Administradores cadastram o integrador autorizado
4. Integrador passa a assinar requisições com sua chave privada
5. API valida a assinatura com a chave pública cadastrada
```

Esse modelo reduz o risco de acesso indevido e aproxima o projeto de uma arquitetura real de comunicação entre microsserviços.

---

# 14. Informações que devem ser enviadas para cadastro

Envie para a equipe da API de Lutas:

```text
Nome do grupo:
Nome da API integradora:
URL do integrador:
Chave pública RSA:
Responsável técnico:
```

Exemplo:

```text
Nome do grupo: Grupo X
Nome da API integradora: api_integrador_grupo_x
URL do integrador: https://meu-integrador.vercel.app
Chave pública RSA:
-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----
Responsável técnico: Nome do aluno
```

---

# 15. Informações que NÃO devem ser enviadas

Nunca envie:

- chave privada;
- senha de ambiente;
- token JWT;
- `.env`;
- credenciais administrativas;
- secrets do provedor.

Apenas a chave pública deve ser compartilhada.

---

# 16. Exemplo de variáveis no ambiente online

Na Vercel, Render ou Railway do integrador:

```env
URL_LUTAS=https://betting-api-beta.vercel.app
NOME_INTEGRADOR=api_integrador_grupo_x
PRIVATE_KEY_PEM=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----
```

Após configurar as variáveis, faça redeploy do integrador.

---

# 17. Teste recomendado

Depois que o cadastro for aprovado, teste primeiro a listagem:

```http
GET /lutas/
```

Se funcionar, teste criação:

```http
POST /lutas/
```

Caso receba `403`, verifique:

- se o `nome_api` é exatamente igual ao cadastrado;
- se a chave pública enviada é correspondente à chave privada usada;
- se a rota assinada é exatamente igual à rota chamada;
- se a barra final `/` foi mantida em `/lutas/`.
