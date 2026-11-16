from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas

def get_produtos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProdutoModel).offset(skip).limit(limit).all()

def get_produto(db: Session, produto_id: int):
    produto = db.query(models.ProdutoModel).filter(models.ProdutoModel.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.ProdutoModel(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def update_produto(db: Session, produto_id: int, produto: schemas.ProdutoUpdate):
    db_produto = get_produto(db, produto_id)
    update_data = produto.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_produto, key, value)
        
    db.commit()
    db.refresh(db_produto)
    return db_produto

def delete_produto(db: Session, produto_id: int):
    db_produto = get_produto(db, produto_id)
    db.delete(db_produto)
    db.commit()
    return {"message": "Produto deletado com sucesso"}

def get_estoque_baixo(db: Session):
    return db.query(models.ProdutoModel).filter(models.ProdutoModel.quantidade <= models.ProdutoModel.estoque_minimo).all()