def registrar_tentativa(nome_api, rota, ip, autorizado):
    # Traduz o booleano para um texto legível no log
    status = "AUTORIZADO" if autorizado else "NEGADO"
    
    # Esse print vai aparecer perfeito no painel Functions da Vercel para você monitorar
    print(f"[LOG ACESSO] API: {nome_api} | Rota: {rota} | IP: {ip} | Status: {status}")
    
    try:
        # Funciona na sua máquina local salvando o arquivo texto
        with open("tentativas_acesso.log", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"API: {nome_api} | Rota: {rota} | IP: {ip} | Status: {status}\n")
    except OSError:
        # Evita que a API caia por causa do sistema Read-only da Vercel
        pass