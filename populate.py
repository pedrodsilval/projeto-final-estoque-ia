"""Script para popular o banco de dados de estoque com dados de teste realistas."""

from __future__ import annotations

import sys
from pathlib import Path

# Garante import local dos módulos
sys.path.insert(0, str(Path(__file__).parent))

from database import Base, SessionLocal, engine
import models

PRODUTOS_EXEMPLO = [
    # Eletrônicos
    {"nome": "Notebook Gamer Core i7", "categoria": "Eletrônicos", "quantidade": 4, "estoque_minimo": 5, "preco": 5400.00},
    {"nome": "Mouse Sem Fio Ergonômico", "categoria": "Eletrônicos", "quantidade": 25, "estoque_minimo": 10, "preco": 120.00},
    {"nome": "Teclado Mecânico RGB", "categoria": "Eletrônicos", "quantidade": 2, "estoque_minimo": 6, "preco": 350.00},
    {"nome": "Monitor 27' 144Hz", "categoria": "Eletrônicos", "quantidade": 8, "estoque_minimo": 4, "preco": 1250.00},
    {"nome": "Headset Gamer 7.1", "categoria": "Eletrônicos", "quantidade": 15, "estoque_minimo": 5, "preco": 280.00},
    # Insumos / Escritório
    {"nome": "Papel A4 Chamex 500fls", "categoria": "Insumos", "quantidade": 50, "estoque_minimo": 20, "preco": 28.50},
    {"nome": "Cartucho de Toner HP Preto", "categoria": "Insumos", "quantidade": 3, "estoque_minimo": 5, "preco": 180.00},
    {"nome": "Caneta Esferográfica Azul Cx 50", "categoria": "Insumos", "quantidade": 12, "estoque_minimo": 8, "preco": 45.00},
    # Limpeza
    {"nome": "Desinfetante Hospitalar 5L", "categoria": "Limpeza", "quantidade": 18, "estoque_minimo": 10, "preco": 42.00},
    {"nome": "Detergente Neutro 5L", "categoria": "Limpeza", "quantidade": 5, "estoque_minimo": 8, "preco": 25.00},
    {"nome": "Papel Toalha Interfolha Fd", "categoria": "Limpeza", "quantidade": 30, "estoque_minimo": 15, "preco": 65.00},
    {"nome": "Álcool em Gel 70% 1L", "categoria": "Limpeza", "quantidade": 2, "estoque_minimo": 10, "preco": 16.90},
]


def populate():
    """Cria tabelas se não existirem e insere produtos de teste."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        total_atual = db.query(models.ProdutoModel).count()
        if total_atual > 0:
            print(f"[populate] Banco já contém {total_atual} produto(s). Limpando dados antigos para resetar...")
            db.query(models.ProdutoModel).delete()
            db.commit()

        for item in PRODUTOS_EXEMPLO:
            prod = models.ProdutoModel(**item)
            db.add(prod)
        db.commit()
        print(f"[populate] Sucesso! {len(PRODUTOS_EXEMPLO)} produtos cadastrados com sucesso no estoque.")
    finally:
        db.close()


if __name__ == "__main__":
    populate()
