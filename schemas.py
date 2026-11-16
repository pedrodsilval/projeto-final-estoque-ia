from pydantic import BaseModel, Field
from datetime import datetime

class ProdutoBase(BaseModel):
    nome: str = Field(..., example="Notebook Gamer")
    categoria: str = Field(..., example="Eletrônicos")
    quantidade: int = Field(..., ge=0, example=10)
    estoque_minimo: int = Field(..., ge=0, example=3)
    preco: float = Field(..., gt=0, example=4500.00)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    nome: str | None = None
    categoria: str | None = None
    quantidade: int | None = Field(None, ge=0)
    estoque_minimo: int | None = Field(None, ge=0)
    preco: float | None = Field(None, gt=0)

class ProdutoResponse(ProdutoBase):
    id: int
    atualizado_em: datetime

    class Config:
        from_attributes = True

class PerguntaIARequest(BaseModel):
    pergunta: str = Field(..., example="Quais produtos estão acabando e qual o valor total de eletrônicos?")

class PerguntaIAResponse(BaseModel):
    pergunta: str
    resposta: str

class RelatorioIAResponse(BaseModel):
    relatorio: str
