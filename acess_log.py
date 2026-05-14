def registrar_tentativa(username, ip, status, motivo):
    print(f"[LOG] Tentativa: {username} | IP: {ip} | Status: {status} | Motivo: {motivo}")
    try:
        with open("tentativas_acesso.log", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{username} | {ip} | {status} | {motivo}\n")
    except OSError:
        # Força a Vercel a ignorar o erro de escrita de arquivo e continuar a rota
        pass