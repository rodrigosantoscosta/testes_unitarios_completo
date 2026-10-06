import pytest
from tech.angelofdiasg.qabank.operacoes.validador_conta import validar_abertura_conta

# Testes gerados com base nos "cenários_iniciais.txt"
# Abordagem de código repetitivo (cada cenário é uma função separada)

def test_cenario_caminho_feliz_aprovado():
    """Testa um cliente comum com boa idade e bom score."""
    resultado = validar_abertura_conta(idade=25, score_credito=800)
    assert resultado == "Aprovado"

def test_cenario_idade_valida_score_baixo_recusado():
    """Testa um cliente maior de idade, mas com score reprovado."""
    resultado = validar_abertura_conta(idade=30, score_credito=200)
    assert resultado == "Recusado"

def test_cenario_menor_idade_score_alto_gera_erro():
    """Testa um menor de idade. O sistema deve lançar erro ignorando o score."""
    with pytest.raises(ValueError, match="Menor de idade não permitido"):
        validar_abertura_conta(idade=15, score_credito=900)

def test_cenario_menor_idade_score_baixo_gera_erro():
    """Testa um menor de idade com score também baixo."""
    with pytest.raises(ValueError, match="Menor de idade não permitido"):
        validar_abertura_conta(idade=10, score_credito=100)
