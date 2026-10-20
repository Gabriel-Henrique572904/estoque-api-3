from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Importa a dependência da base de dados e o serviço de IA recém-criado
from app.database import get_db
from app.services import ia as ia_service

# Define o router com o prefixo /ia
router = APIRouter(prefix="/ia", tags=["Inteligência Artificial"])

@router.get("/relatorio-estoque")
def obter_relatorio_inteligente(db: Session = Depends(get_db)):
    """
    Analisa os produtos na base de dados e utiliza uma LLM (Gemini) para gerar recomendações de reposição.
    """
    # Chama a função gerar_analise_estoque do serviço de IA
    return ia_service.gerar_analise_estoque(db)