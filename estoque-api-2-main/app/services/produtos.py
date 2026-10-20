from sqlalchemy.orm import Session
from app import models

def get_produtos(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    nome: str = None, 
    categoria_id: int = None
):
    # Inicia a consulta na tabela de produtos
    query = db.query(models.Produto)
    
    # Aplica o filtro de nome, se foi informado na URL (usa ilike para ignorar maiúsculas/minúsculas)
    if nome:
        query = query.filter(models.Produto.nome.ilike(f"%{nome}%"))
        
    # Aplica o filtro de categoria, se foi informado na URL
    if categoria_id:
        query = query.filter(models.Produto.categoria_id == categoria_id)
        
    # Aplica a paginação no final da consulta e retorna os resultados
    return query.offset(skip).limit(limit).all()