import os
import requests
from sqlalchemy.orm import Session
from app import models
from app.config import settings

def gerar_analise_estoque(db: Session):
    # Obtém a chave do settings ou do ambiente
    chave_api = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")
    if not chave_api:
        return {"erro": "Chave da API não configurada."}

    # 1. Obter dados reais das regras de negócio
    produtos = db.query(models.Produto).all()
    produtos_criticos = [p for p in produtos if p.quantidade < 10]
    
    if not produtos_criticos:
        return {"relatorio": "O stock está saudável. Não há produtos em estado crítico no momento."}
    
    # 2. Montar o contexto para a LLM
    detalhes_produtos = ", ".join([f"{p.nome} (Qtd: {p.quantidade})" for p in produtos_criticos])
    prompt = (
        "Atuas como um consultor de inteligência artificial especializado em otimizar a operação de empresas locais. "
        "O sistema de gestão identificou que os seguintes produtos estão com stock crítico: "
        f"{detalhes_produtos}. "
        "Gera um relatório curto (máximo de 3 parágrafos) com sugestões de reposição, prioridades de compra e como evitar a rutura deste inventário."
    )
    
    # 3. Chamar a LLM via REST API (sem usar a biblioteca google-generativeai)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={chave_api}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        resposta = requests.post(url, json=payload)
        resposta.raise_for_status() # Verifica se houve erro no pedido HTTP
        dados = resposta.json()
        
        # Extrai o texto da resposta JSON da Google
        texto_gerado = dados["candidates"][0]["content"]["parts"][0]["text"]
        return {"relatorio": texto_gerado}
    except Exception as e:
        return {"erro": f"Falha ao gerar relatório inteligente: {str(e)}"}