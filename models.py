from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Luta(Base):
    __tablename__ = "lutas"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False)
    horario = Column(String, nullable=False)
    id_lutador1 = Column(Integer, nullable=False)
    id_lutador2 = Column(Integer, nullable=False)

class IntegradorAutorizado(Base):
    __tablename__ = "integradores_autorizados"
    id = Column(Integer, primary_key=True, index=True)
    nome_api = Column(String, unique=True, nullable=False)
    chave_publica_pem = Column(Text, nullable=False)
    ativo = Column(Integer, default=1)