import copy

import pytest

from tech.angelofdiasg.qabank.operacoes.validar_saque import validar_saque


@pytest.fixture
def saque_base():
    """Fornece um pedido válido para ser adaptado em cada teste."""
    return {
        "valor": 300,
        "conta": {
            "tipo": "corrente",
            "saldo": 1200,
            "total_sacado_hoje": 400,
        },
    }


# ----------------------------------------------------------------------
# Caminho feliz
# ----------------------------------------------------------------------
def test_caminho_feliz_aprovado(saque_base):
    resultado = validar_saque(saque_base)

    assert resultado == {
        "status": "Aprovado",
        "motivo": "Saque autorizado",
        "saldo_restante": 900,
    }


# ----------------------------------------------------------------------
# Limites e partições válidas (limite diário por tipo de conta)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "tipo, valor, total_sacado_hoje, status_esperado, motivo_esperado",
    [
        pytest.param(
            "corrente", 500, 1500, "Aprovado", "Saque autorizado",
            id="corrente-no-limite-diario",
        ),
        pytest.param(
            "corrente", 501, 1500, "Recusado", "Limite diário de saque excedido",
            id="corrente-acima-do-limite-diario",
        ),
        pytest.param(
            "poupanca", 300, 700, "Aprovado", "Saque autorizado",
            id="poupanca-no-limite-diario",
        ),
        pytest.param(
            "poupanca", 301, 700, "Recusado", "Limite diário de saque excedido",
            id="poupanca-acima-do-limite-diario",
        ),
    ],
)
def test_validar_saque_por_tipo_e_limite_diario(
    saque_base,
    tipo,
    valor,
    total_sacado_hoje,
    status_esperado,
    motivo_esperado,
):
    saque_base["conta"]["tipo"] = tipo
    saque_base["valor"] = valor
    saque_base["conta"]["total_sacado_hoje"] = total_sacado_hoje

    resultado = validar_saque(saque_base)

    assert resultado["status"] == status_esperado
    assert resultado["motivo"] == motivo_esperado


@pytest.mark.parametrize(
    "valor, saldo, status_esperado, motivo_esperado, saldo_restante_esperado",
    [
        pytest.param(
            1000, 1000, "Aprovado", "Saque autorizado", 0,
            id="saldo-exatamente-suficiente",
        ),
        pytest.param(
            1001, 1000, "Recusado", "Saldo insuficiente", 1000,
            id="saldo-um-real-insuficiente",
        ),
    ],
)
def test_limites_de_saldo(
    saque_base, valor, saldo, status_esperado, motivo_esperado, saldo_restante_esperado
):
    saque_base["valor"] = valor
    saque_base["conta"]["saldo"] = saldo
    saque_base["conta"]["total_sacado_hoje"] = 0

    resultado = validar_saque(saque_base)

    assert resultado["status"] == status_esperado
    assert resultado["motivo"] == motivo_esperado
    assert resultado["saldo_restante"] == saldo_restante_esperado


# ----------------------------------------------------------------------
# Partições inválidas e exceções
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "entrada",
    [
        pytest.param(None, id="entrada-none"),
        pytest.param({}, id="dicionario-vazio"),
        pytest.param(
            {"conta": {"tipo": "corrente", "saldo": 1200, "total_sacado_hoje": 400}},
            id="sem-valor",
        ),
        pytest.param({"valor": 300}, id="sem-conta"),
        pytest.param(
            {"valor": 300, "conta": {"tipo": "corrente", "saldo": 1200}},
            id="conta-incompleta",
        ),
    ],
)
def test_dados_invalidos_lancam_value_error(entrada):
    with pytest.raises(ValueError, match="Dados do saque inválidos"):
        validar_saque(entrada)


@pytest.mark.parametrize(
    "valor, motivo_esperado",
    [
        pytest.param(
            -10, "Valor do saque deve ser maior que zero", id="valor-negativo"
        ),
        pytest.param(0, "Valor do saque deve ser maior que zero", id="valor-zero"),
    ],
)
def test_valor_nao_positivo_e_recusado(saque_base, valor, motivo_esperado):
    saque_base["valor"] = valor

    resultado = validar_saque(saque_base)

    assert resultado["status"] == "Recusado"
    assert resultado["motivo"] == motivo_esperado
    assert resultado["saldo_restante"] == saque_base["conta"]["saldo"]


def test_tipo_de_conta_invalido_e_recusado(saque_base):
    saque_base["conta"]["tipo"] = "investimento"

    resultado = validar_saque(saque_base)

    assert resultado == {
        "status": "Recusado",
        "motivo": "Tipo de conta inválido",
        "saldo_restante": 1200,
    }


# ----------------------------------------------------------------------
# Prioridade entre regras (critério 6: tipo -> valor -> saldo -> limite)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "valor, tipo, saldo, total_sacado_hoje, motivo_esperado",
    [
        pytest.param(
            -10, "carteira", 500, 0, "Tipo de conta inválido",
            id="tipo-invalido-sobrevalor-negativo",
        ),
        pytest.param(
            -10, "corrente", 0, 0, "Valor do saque deve ser maior que zero",
            id="valor-negativo-sobre-saldo-insuficiente",
        ),
        pytest.param(
            3000, "corrente", 100, 1900, "Saldo insuficiente",
            id="saldo-insuficiente-sobre-limite-diario",
        ),
    ],
)
def test_prioridade_entre_regras(
    saque_base, valor, tipo, saldo, total_sacado_hoje, motivo_esperado
):
    saque_base["valor"] = valor
    saque_base["conta"]["tipo"] = tipo
    saque_base["conta"]["saldo"] = saldo
    saque_base["conta"]["total_sacado_hoje"] = total_sacado_hoje

    resultado = validar_saque(saque_base)

    assert resultado["status"] == "Recusado"
    assert resultado["motivo"] == motivo_esperado


# ----------------------------------------------------------------------
# Integridade dos dados de entrada (critério 9)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "valor",
    [pytest.param(300, id="aprovado"), pytest.param(9999, id="recusado")],
)
def test_entrada_nao_e_alterada(saque_base, valor):
    saque_base["valor"] = valor
    original = copy.deepcopy(saque_base)

    validar_saque(saque_base)

    assert saque_base == original
