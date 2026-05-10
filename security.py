import base64   
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def chave_publica(caminho="public_key.pem"):
    with open(caminho, "rb") as f:
        return serialization.load_pem_public_key(f.read())
    
def verificar_assinatura(mensagem: str, assinatura_base64: str) -> bool:
    try:
        public_key = chave_publica()

        assinatura = base64.b64decode(assinatura_base64)

        public_key.verify(
            assinatura,
            mensagem.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True

    except InvalidSignature:
        return False

    except Exception as erro:
        print("Erro ao verificar a assinatura:", erro)
        return False