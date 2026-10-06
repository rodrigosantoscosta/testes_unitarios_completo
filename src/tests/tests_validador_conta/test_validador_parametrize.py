import pytest
from tech.angelofdiasg.qabank.operacoes.validador_conta import validar_abertura_conta

# Parametrize (@pytest.mark.parametrize)
# O que é: É uma tabela de dados (Data-Driven Testing). Você fornece uma lista de cenários diferentes.

# Qual o objetivo: Rodar a mesma função de teste múltiplas vezes, apenas trocando as variáveis de entrada.

# Quando usar:

#   Quando você tem uma Tabela de Decisão.

#   Quando precisa testar vários números em uma calculadora (Ex: 2+2, -5+3, 0+0).

#   Quando precisa testar várias idades no validador (Ex: 17, 18, 19).

# Como funciona: Se você passar 5 linhas no parametrize, o Pytest vai rodar o teste 5 vezes independentes.

@pytest.mark.parametrize("idade, score_credito, resultado_esperado", [
    (25, 800, "Aprovado"),      # Cenário 1: Caminho feliz
    (30, 200, "Recusado"),      # Cenário 2: Score baixo
    (18, 600, "Aprovado"),      # Cenário 3: Limite de idade
    (40, 500, "Recusado"),      # Cenário 4: Limite de score
])
def test_validador_conta_retornos(idade, score_credito, resultado_esperado):
    """Testa os cenários que retornam 'Aprovado' ou 'Recusado'."""
    resultado = validar_abertura_conta(idade, score_credito)
    assert resultado == resultado_esperado

@pytest.mark.parametrize("idade, score_credito", [
    (17, 900),      # Menor de idade com score alto
    (10, 100),      # Menor de idade com score baixo
    (0, 500),       # Idade zero
])
def test_validador_conta_excecoes(idade, score_credito):
    """Testa os cenários de exceção para menores de idade."""
    with pytest.raises(ValueError, match="Menor de idade não permitido"):
        validar_abertura_conta(idade, score_credito)