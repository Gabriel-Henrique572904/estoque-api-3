from fastapi.testclient import TestClient
from app.main import app

# Cria um cliente de teste que simula o frontend
client = TestClient(app)

def test_listar_produtos_sucesso():
    """
    Testa se a rota GET /produtos retorna o status 200 e uma lista de dados.
    """
    response = client.get("/produtos/")
    
    # Verifica se o servidor respondeu com sucesso
    assert response.status_code == 200
    
    # Verifica se a resposta é uma lista (mesmo que esteja vazia)
    assert isinstance(response.json(), list)

def test_listar_produtos_com_paginacao():
    """
    Testa se a paginação (limit) está a ser respeitada.
    """
    response = client.get("/produtos/?skip=0&limit=5")
    assert response.status_code == 200
    
    dados = response.json()
    # Verifica se não retorna mais do que os 5 itens pedidos
    assert len(dados) <= 5