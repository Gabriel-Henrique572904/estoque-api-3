from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import categorias, produtos, movimentacoes, ia

# 1. Adicione estas duas importações
from app.database import engine
from app import models

app = FastAPI(
    title="Estoque API - Checkpoint 2",
    description="API para gestão de estoque com integração de IA",
    version="1.0.0"
)

# 2. Adicione este comando para criar as tabelas automaticamente
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(movimentacoes.router)
app.include_router(ia.router)

@app.get("/")
def read_root():
    return {"mensagem": "API de Estoque do Checkpoint 2 a funcionar corretamente!"}