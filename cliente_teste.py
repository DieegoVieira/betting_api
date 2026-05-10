import base64
import requests

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def carregar_chave_privada(caminho="private_key.pem"):
    with open(caminho, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )

def assinar_mensagem(mensagem: str) -> str:
    private_key = carregar_chave_privada()

    assinatura = private_key.sign(
        mensagem.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return base64.b64encode(assinatura).decode("utf-8")

nome_api = "api_1"
rota = "/lutas/"
mensagem = f"{nome_api}:{rota}"

print("Mensagem assinada no cliente:", mensagem)

assinatura = assinar_mensagem(mensagem)

headers = {
    "x-api-nome": nome_api,
    "x-assinatura": assinatura
}

resposta = requests.get(
    "http://127.0.0.1:8001/lutas/",
    headers=headers
)

print(resposta.status_code)
print(resposta.json())