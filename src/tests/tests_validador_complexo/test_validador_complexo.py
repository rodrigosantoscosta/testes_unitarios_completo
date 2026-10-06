import pytest
from tech.angelofdiasg.qabank.operacoes.validador_complexo import validar_cliente_premium

# ====================================================================
# Nota Didática: A fixture 'cliente_base' foi movida para tests/conftest.py.
# Repare que NÃO há 'import cliente_base'. O Pytest faz essa injeção
# de dependência magicamente por debaixo dos panos!
# ====================================================================

def test_cliente_premium_aprovado(cliente_base):
    """Cenário 1: Tudo Perfeito. Usamos a fixture inalterada."""
    resultado = validar_cliente_premium(cliente_base)
    
    assert resultado["status"] == "Aprovado"

def test_recusar_menor_de_idade(cliente_base):
    """
    Cenário 2: Pegamos o cliente base e alteramos APENAS a idade.
    Isso mostra o poder da Fixture: não precisamos recriar a morada
    ou os dados financeiros para testar a idade.
    """
    # Alteramos a idade na cópia injetada
    cliente_base["idade"] = 17 
    
    resultado = validar_cliente_premium(cliente_base)
    
    assert resultado["status"] == "Recusado"
    assert "Idade inferior" in resultado["motivo"]

def test_recusar_morada_sem_cep(cliente_base):
    """Cenário 3: Manipulação de dados aninhados (Dicionário dentro de Dicionário)"""
    cliente_base["morada"]["cep"] = "" # Limpamos o CEP
    
    resultado = validar_cliente_premium(cliente_base)
    
    assert resultado["status"] == "Recusado"
    assert "Código postal" in resultado["motivo"]

def test_recusar_score_baixo(cliente_base):
    """Cenário 4: Manipulando dados financeiros na fixture."""
    cliente_base["dados_financeiros"]["score_credito"] = 699
    
    resultado = validar_cliente_premium(cliente_base)
    
    assert resultado["status"] == "Recusado"
    assert "Score de crédito" in resultado["motivo"]

def test_excecao_dados_invalidos():
    """Cenário 5: Teste de exceção. Não usamos a fixture aqui pois passamos 'None'."""
    with pytest.raises(ValueError, match="Dados do cliente inválidos"):
        validar_cliente_premium(None)