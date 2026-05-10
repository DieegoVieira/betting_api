from datetime import datetime

def registrar_tentativa(nome_api: str, rota: str, ip: str, autorizado: bool):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    status = "AUTORIZADO" if autorizado else "NEGADO"

    linha = (
        f"[{data_hora}]"
        f"API: {nome_api} |"
        f"IP: {ip} |"
        f"Rota: {rota} |"
        f"Status: {status}\n"
    )

    with open("tentativas_acesso.log", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)