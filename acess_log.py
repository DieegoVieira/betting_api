def registrar_tentativa(username, ip, status, motivo):
    # O print manda o log para o painel da Vercel para você monitorar
    print(f"[LOG] Tentativa: {username} | IP: {ip} | Status: {status} | Motivo: {motivo}")
    
    try:
        # Funciona no seu computador local, mas vai falhar na Vercel
        with open("tentativas_acesso.log", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{username} | {ip} | {status} | {motivo}\n")
    except OSError:
        # Se der erro de Read-only na Vercel, o Python ignora e a API continua rodando lindamente!
        pass