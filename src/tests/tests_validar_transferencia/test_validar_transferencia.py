import pytest

from tech.angelofdiasg.qabank.operacoes.validar_transferencia import (
    validar_transferencia,
)


@pytest.fixture
def transferencia_valida():
    """Transferência válida e isolada: cada teste recebe a sua própria cópia."""
    return {
        "valor": 250,
        "conta_origem": {
            "numero": "12345",
            "tipo": "corrente",
            "saldo": 1200,
        },
        "conta_destino": {
            "numero": "67890",
        },
    }


# ----------------------------------------------------------------------
# Cenário 1: caminho feliz
# ----------------------------------------------------------------------
def test_transferencia_valida_aprovada(transferencia_valida):
    resultado = validar_transferencia(transferencia_valida)

    assert resultado == {
        "status": "Aprovada",
        "motivo": "Transferência autorizada",
    }


# ----------------------------------------------------------------------
# Cenários 2-5: limites por tipo de conta (regra 6)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "tipo, valor, status_esperado, motivo_esperado",
    [
        pytest.param(
            "corrente", 1000, "Aprovada", "Transferência autorizada",
            id="corrente-no-limite",
        ),
        pytest.param(
            "corrente", 1001, "Recusada", "Limite de transferência excedido",
            id="corrente-acima-do-limite",
        ),
        pytest.param(
            "poupanca", 500, "Aprovada", "Transferência autorizada",
            id="poupanca-no-limite",
        ),
        pytest.param(
            "poupanca", 501, "Recusada", "Limite de transferência excedido",
            id="poupanca-acima-do-limite",
        ),
    ],
)
def test_limites_por_tipo_de_conta(
    transferencia_valida, tipo, valor, status_esperado, motivo_esperado
):
    transferencia_valida["conta_origem"]["tipo"] = tipo
    transferencia_valida["valor"] = valor
    transferencia_valida["conta_origem"]["saldo"] = 5000

    resultado = validar_transferencia(transferencia_valida)

    assert resultado["status"] == status_esperado
    assert resultado["motivo"] == motivo_esperado


# ----------------------------------------------------------------------
# Cenário 6: valor inválido (regra 4)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "valor",
    [pytest.param(0, id="valor-zero"), pytest.param(-100, id="valor-negativo")],
)
def test_valor_invalido_recusado(transferencia_valida, valor):
    transferencia_valida["valor"] = valor

    resultado = validar_transferencia(transferencia_valida)

    assert resultado == {
        "status": "Recusada",
        "motivo": "Valor da transferência deve ser maior que zero",
    }


# ----------------------------------------------------------------------
# Cenário 7: saldo insuficiente (regra 5)
# ----------------------------------------------------------------------
def test_saldo_insuficiente_recusado(transferencia_valida):
    transferencia_valida["valor"] = 1500
    transferencia_valida["conta_origem"]["saldo"] = 1000

    resultado = validar_transferencia(transferencia_valida)

    assert resultado == {"status": "Recusada", "motivo": "Saldo insuficiente"}


# ----------------------------------------------------------------------
# Cenário 8: contas iguais (regra 3)
# ----------------------------------------------------------------------
def test_contas_iguais_recusado(transferencia_valida):
    transferencia_valida["conta_destino"]["numero"] = (
        transferencia_valida["conta_origem"]["numero"]
    )

    resultado = validar_transferencia(transferencia_valida)

    assert resultado == {
        "status": "Recusada",
        "motivo": "Contas de origem e destino devem ser diferentes",
    }


# ----------------------------------------------------------------------
# Cenário 9: tipo de conta inválido (regra 2)
# ----------------------------------------------------------------------
def test_tipo_de_conta_invalido_recusado(transferencia_valida):
    transferencia_valida["conta_origem"]["tipo"] = "investimento"

    resultado = validar_transferencia(transferencia_valida)

    assert resultado == {"status": "Recusada", "motivo": "Tipo de conta inválido"}


# ----------------------------------------------------------------------
# Cenário 10: estrutura inválida -> ValueError (regra 1)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "entrada",
    [
        pytest.param(None, id="entrada-none"),
        pytest.param({}, id="dicionario-vazio"),
        pytest.param({"valor": 250}, id="sem-contas"),
        pytest.param(
            {
                "valor": 250,
                "conta_origem": {"numero": "12345", "tipo": "corrente"},
                "conta_destino": {"numero": "67890"},
            },
            id="origem-sem-saldo",
        ),
        pytest.param(
            {
                "valor": 250,
                "conta_origem": {
                    "numero": "12345",
                    "tipo": "corrente",
                    "saldo": 1200,
                },
                "conta_destino": {},
            },
            id="destino-sem-numero",
        ),
    ],
)
def test_estrutura_invalida_lanca_value_error(entrada):
    with pytest.raises(ValueError, match="Dados da transferência inválidos"):
        validar_transferencia(entrada)

