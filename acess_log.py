from datetime import datetime

def registrar_tentativa(username, ip, status, motivo):
    # Mantém o print para você ver o log rodando no painel da Vercel
    print(f"[LOG] Tentativa: {username} | IP: {ip} | Status: {status} | Motivo: {motivo}")
    
    try:
        # Tenta salvar no arquivo (vai funcionar no seu PC, mas vai falhar na Vercel)
        with open("tentativas_acesso.log", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{username} | {ip} | {status} | {motivo}\n")
    except OSError:
        # Se der erro de Read-only na Vercel, ele ignora e a API não quebra!
        pass