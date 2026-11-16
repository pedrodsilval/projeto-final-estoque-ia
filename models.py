from sqlalchemy import Column, Float, Integer, String, DateTime
from datetime import datetime
from database import Base

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    categoria = Column(String, index=True, nullable=False)
    quantidade = Column(Integer, nullable=False)
    estoque_minimo = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)