from models import LogAcesso

def registrar_tentativa(nome_api, rota, ip, autorizado, SessionLocal):
    status_texto = "AUTORIZADO" if autorizado else "NEGADO"
    
    # Esse print continuará aparecendo em tempo real no console da Vercel
    print(f"[LOG ACESSO] API: {nome_api} | Rota: {rota} | IP: {ip} | Status: {status_texto}")
    
    # Abre uma sessão rápida com o banco para persistir o log
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
        db.close() # Garante que a conexão do Neon seja liberada