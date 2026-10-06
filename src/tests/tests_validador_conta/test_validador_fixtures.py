import pytest
from tech.angelofdiasg.qabank.operacoes.validador_conta import validar_abertura_conta


# Fixtures (@pytest.fixture)
# O que é: É uma função de preparação. Ela cria o "ambiente" ou os "dados pesados" que o seu teste precisa antes de rodar.

# Qual o objetivo: Reutilizar configuração. (Injeção de Dependência).

# Quando usar:

#   Quando você precisa abrir um navegador (Selenium).

#   Quando precisa conectar a um banco de dados.

#   Quando precisa criar um usuário falso complexo no sistema com nome, email, CPF e senha para usar no teste.

# Como funciona: O teste roda uma vez, pegando o "pacote" pronto que a fixture entregou.

@pytest.fixture
def base_de_clientes():
    """
    FIXTURE: Prepara e fornece os dados para os testes.
    Na vida real de um QA, isto poderia ser uma consulta à base de dados,
    a leitura de um ficheiro JSON, ou a geração de um utilizador falso.
    """
    return {
        "perfil_ideal": {"idade": 25, "score": 800, "esperado": "Aprovado"},
        "perfil_score_baixo": {"idade": 30, "score": 200, "esperado": "Recusado"},
        "perfil_menor_idade": {"idade": 16, "score": 900} # Esperamos que dê erro
    }

def test_deve_aprovar_perfil_ideal(base_de_clientes):
    """
    O Pytest percebe que 'base_de_clientes' é uma fixture e injeta 
    o dicionário inteiro aqui dentro automaticamente.
    """
    cliente = base_de_clientes["perfil_ideal"]
    
    resultado = validar_abertura_conta(cliente["idade"], cliente["score"])
    
    assert resultado == cliente["esperado"]

def test_deve_recusar_perfil_com_score_baixo(base_de_clientes):
    cliente = base_de_clientes["perfil_score_baixo"]
    
    resultado = validar_abertura_conta(cliente["idade"], cliente["score"])
    
    assert resultado == cliente["esperado"]

def test_deve_bloquear_menor_de_idade(base_de_clientes):
    cliente = base_de_clientes["perfil_menor_idade"]
    
    # Valida se o sistema levanta (raises) o erro corretamente
    with pytest.raises(ValueError, match="Menor de idade não permitido"):
        validar_abertura_conta(cliente["idade"], cliente["score"])