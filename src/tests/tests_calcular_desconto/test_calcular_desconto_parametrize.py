import pytest
from tech.angelofdiasg.qabank.operacoes.calcular_desconto import calcular_desconto

# ====================================================================
# PARTE 2: TESTES COM PARAMETRIZE (Data-Driven Testing)
# Ideal para testar regras matemáticas e limites!
# É a solução mais elegante para este tipo específico de problema (regras matemáticas simples).
# ====================================================================

@pytest.mark.parametrize("valor_compra, valor_esperado", [
    (0, 0),             # Limite inferior sem desconto
    (100, 100),         # Limite superior sem desconto
    (101, 90.9),        # Limite inferior 10%
    (300, 270),         # Equivalência 10%
    (500, 450),         # Limite superior 10%
    (501, 400.8),       # Limite inferior 20%
    (1000, 800)         # Equivalência 20%
])
def test_calculo_descontos_validos(valor_compra, valor_esperado):
    """Testa todos os caminhos felizes com uma única função!"""
    assert calcular_desconto(valor_compra) == valor_esperado


def test_desconto_excecao_negativo():
    """Testes de exceção geralmente ficam separados do parametrize."""
    with pytest.raises(ValueError, match="não pode ser negativo"):
        calcular_desconto(-1)