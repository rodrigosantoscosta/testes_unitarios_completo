import pytest
from tech.angelofdiasg.qabank.operacoes.calcular_desconto import calcular_desconto

# ====================================================================
# PARTE 3: TESTES COM FIXTURES (Injeção de Dependência)
# Simulando uma leitura de carrinho de compras de uma loja.
# Não é a técnica ideal para testar uma matemática simples, mas é perfeita se o calcular_desconto 
# recebesse um "Objeto Cliente" completo e complexo (com histórico de compras, morada, etc.) em vez de apenas um número
# ====================================================================

@pytest.fixture
def carrinhos_de_compra():
    """
    Simula uma Base de Dados retornando diferentes "carrinhos" fechados.
    """
    return {
        "carrinho_pequeno": {"total": 50, "esperado": 50},
        "carrinho_medio": {"total": 200, "esperado": 180},
        "carrinho_grande": {"total": 800, "esperado": 640},
        "carrinho_invalido": {"total": -50}
    }

def test_desconto_carrinho_pequeno(carrinhos_de_compra):
    dados = carrinhos_de_compra["carrinho_pequeno"]
    assert calcular_desconto(dados["total"]) == dados["esperado"]

def test_desconto_carrinho_medio(carrinhos_de_compra):
    dados = carrinhos_de_compra["carrinho_medio"]
    assert calcular_desconto(dados["total"]) == dados["esperado"]

def test_desconto_carrinho_grande(carrinhos_de_compra):
    dados = carrinhos_de_compra["carrinho_grande"]
    assert calcular_desconto(dados["total"]) == dados["esperado"]

def test_desconto_carrinho_invalido(carrinhos_de_compra):
    dados = carrinhos_de_compra["carrinho_invalido"]
    with pytest.raises(ValueError):
        calcular_desconto(dados["total"])