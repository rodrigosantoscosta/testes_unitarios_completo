import pytest

@pytest.fixture
def cliente_base():
    """
    FIXTURE GLOBAL: Cria o 'Payload' base de um cliente perfeito.
    
    Como este código está no ficheiro 'conftest.py', o Pytest carrega
    esta fixture automaticamente. Qualquer ficheiro de teste dentro da pasta
    'tests' pode usar o 'cliente_base' sem precisar de fazer 'import'!
    """
    return {
        "nome": "João Silva",
        "idade": 30,
        "morada": {
            "rua": "Av. Liberdade",
            "cidade": "Lisboa",
            "cep": "1250-001"
        },
        "dados_financeiros": {
            "score_credito": 850,
            "renda_mensal": 6000.00
        }
    }