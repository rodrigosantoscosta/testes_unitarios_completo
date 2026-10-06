import pytest
from tech.angelofdiasg.qabank.operacoes.calcular_desconto import calcular_desconto

# ====================================================================
# PARTE 1: TESTES DIRETOS (Abordagem Ingénua)
# Um teste para cada cenário, com repetição de código.
# ====================================================================

def test_desconto_valor_negativo():
    with pytest.raises(ValueError, match="não pode ser negativo"):
        calcular_desconto(-10)

def test_desconto_zero():
    assert calcular_desconto(0) == 0

def test_desconto_limite_sem_desconto():
    assert calcular_desconto(100) == 100

def test_desconto_limite_inicio_10_porcento():
    assert calcular_desconto(101) == 90.9

def test_desconto_meio_10_porcento():
    assert calcular_desconto(300) == 270

def test_desconto_limite_fim_10_porcento():
    assert calcular_desconto(500) == 450

def test_desconto_limite_inicio_20_porcento():
    assert calcular_desconto(501) == 400.8

def test_desconto_meio_20_porcento():
    assert calcular_desconto(1000) == 800