from models import LogAcesso

def registrar_tentativa(nome_api, rota, ip, autorizado):
    status_texto = "AUTORIZADO" if autorizado else "NEGADO"
    print(f"[LOG] API: {nome_api} | Rota: {rota} | IP: {ip} | Status: {status_texto}")
    
    # Aqui usamos uma estratégia alternativa pura para criar a sessão direto no arquivo de log
    from API_lutas import SessionLocal
    db = SessionLocal()
    try:
        novo_log = LogAcesso(
            nome_api=nome_api or "DESCONHECIDA",
            rota=rota,
            ip=ip,
            status=status_texto
        )
        db.add(novo_log)
        db.commit()
    except Exception as e:
        print(f"[ERRO AO SALVAR LOG NO BANCO]: {str(e)}")
        db.rollback()
    finally:
        db.close()