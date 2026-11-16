"""Servidor FastAPI e rotas da API para gerenciamento de estoque e IA."""

from __future__ import annotations

import sys
from pathlib import Path

# Garante import local dos módulos do projeto
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import crud
import schemas
import ai_service

# Cria as tabelas do banco automaticamente na inicialização
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gerenciamento de Estoque com IA",
    description="Projeto Final de Machine Learning e Deep Learning - FastAPI + SQLAlchemy + Pandas + Ollama",
    version="1.0.0",
)


# ==========================================
# 1. Rotas de Produtos (CRUD e Alertas)
# ==========================================

@app.get("/produtos/", response_model=list[schemas.ProdutoResponse], tags=["Produtos"])
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os produtos cadastrados com paginação opcional."""
    return crud.get_produtos(db, skip=skip, limit=limit)


@app.post(
    "/produtos/",
    response_model=schemas.ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Produtos"],
)
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    """Cadastra um novo produto no estoque."""
    return crud.create_produto(db, produto=produto)


@app.get("/produtos/alerta-baixo", response_model=list[schemas.ProdutoResponse], tags=["Produtos"])
def listar_produtos_alerta_baixo(db: Session = Depends(get_db)):
    """Retorna produtos que estão com quantidade igual ou abaixo do estoque mínimo."""
    return crud.get_estoque_baixo(db)


@app.get("/produtos/{id}", response_model=schemas.ProdutoResponse, tags=["Produtos"])
def consultar_produto(id: int, db: Session = Depends(get_db)):
    """Consulta um produto específico pelo seu ID."""
    return crud.get_produto(db, produto_id=id)


@app.put("/produtos/{id}", response_model=schemas.ProdutoResponse, tags=["Produtos"])
def atualizar_produto(id: int, produto: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados cadastrais ou o saldo em estoque de um produto."""
    return crud.update_produto(db, produto_id=id, produto=produto)


@app.delete("/produtos/{id}", tags=["Produtos"])
def remover_produto(id: int, db: Session = Depends(get_db)):
    """Remove um produto do estoque pelo seu ID."""
    return crud.delete_produto(db, produto_id=id)


# ==========================================
# 2. Rotas de Inteligência Artificial (Pandas + Ollama)
# ==========================================

@app.post("/ia/pergunta", response_model=schemas.PerguntaIAResponse, tags=["Inteligência Artificial"])
def perguntar_para_ia(payload: schemas.PerguntaIARequest, db: Session = Depends(get_db)):
    """Envia uma pergunta em linguagem natural para a IA analisar o estoque usando Pandas + Ollama."""
    try:
        resposta = ai_service.responder_pergunta_estoque(db, payload.pergunta)
        return schemas.PerguntaIAResponse(pergunta=payload.pergunta, resposta=resposta)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar IA (Ollama): {exc}",
        )


@app.get("/ia/relatorio", response_model=schemas.RelatorioIAResponse, tags=["Inteligência Artificial"])
def gerar_relatorio_ia(db: Session = Depends(get_db)):
    """Gera um resumo executivo automatizado do estoque utilizando Pandas + Ollama."""
    try:
        relatorio = ai_service.gerar_relatorio_executivo(db)
        return schemas.RelatorioIAResponse(relatorio=relatorio)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar relatório via IA (Ollama): {exc}",
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
