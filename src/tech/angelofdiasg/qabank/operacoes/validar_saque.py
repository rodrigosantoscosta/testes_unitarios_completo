LIMITES_DIARIOS = {
    "corrente": 2000,
    "poupanca": 1000,
}


def validar_saque(saque):
    """Valida um pedido de saque segundo os critérios da atividade."""
    # Critério 1: estrutura obrigatória (exceção)
    if not isinstance(saque, dict) or "valor" not in saque or "conta" not in saque:
        raise ValueError("Dados do saque inválidos")

    conta = saque["conta"]
    if (
        not isinstance(conta, dict)
        or "tipo" not in conta
        or "saldo" not in conta
        or "total_sacado_hoje" not in conta
    ):
        raise ValueError("Dados do saque inválidos")

    valor = saque["valor"]
    tipo = conta["tipo"]
    saldo = conta["saldo"]
    total_sacado_hoje = conta["total_sacado_hoje"]

    def recusar(motivo):
        return {
            "status": "Recusado",
            "motivo": motivo,
            "saldo_restante": saldo,
        }

    # Critério 6: ordem das regras -> tipo, valor, saldo, limite diário
    # Critério 2: tipos aceites
    if tipo not in LIMITES_DIARIOS:
        return recusar("Tipo de conta inválido")

    # Critério 3: valor positivo
    if not valor > 0:
        return recusar("Valor do saque deve ser maior que zero")

    # Critério 4: saldo suficiente
    if valor > saldo:
        return recusar("Saldo insuficiente")

    # Critério 5: limite diário (total igual ao limite é permitido)
    if total_sacado_hoje + valor > LIMITES_DIARIOS[tipo]:
        return recusar("Limite diário de saque excedido")

    # Critério 7: aprovação
    return {
        "status": "Aprovado",
        "motivo": "Saque autorizado",
        "saldo_restante": saldo - valor,
    }
