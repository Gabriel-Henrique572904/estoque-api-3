from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

# Importe os seus schemas, services e a dependência do banco de dados
from app import schemas
from app.services import produtos as produto_service
from app.database import get_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=List[schemas.ProdutoResposta])
def listar_produtos(
    # Filtro opcional por nome
    nome: Optional[str] = Query(None, description="Filtrar produtos pelo nome"),
    # Filtro opcional por categoria (VÍRGULA ADICIONADA AQUI)
    categoria_id: Optional[int] = Query(None, description="Filtrar produtos por ID da categoria"),
    # Paginação: quantos itens pular (skip) (VÍRGULA ADICIONADA AQUI)
    skip: int = Query(0, ge=0, description="Número de registros para pular (paginação)"),
    # Paginação: quantos retornar (limit) (VÍRGULA ADICIONADA AQUI)
    limit: int = Query(10, ge=1, le=100, description="Limite de registros por página"),
    db: Session = Depends(get_db)
):
    """
    Lista os produtos do estoque com suporte a paginação e filtros por nome e categoria.
    """
    produtos = produto_service.get_produtos(
        db=db, 
        skip=skip, 
        limit=limit, 
        nome=nome, 
        categoria_id=categoria_id
    )
    
    return produtos