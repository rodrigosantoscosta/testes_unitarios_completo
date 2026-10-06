LIMITES_TRANSFERENCIA = {
    "corrente": 1000,
    "poupanca": 500,
}


def validar_transferencia(transferencia):
    """Valida uma transferência bancária segundo o contrato do desafio."""
    # Regra 1: estrutura obrigatória (exceção)
    if not isinstance(transferencia, dict):
        raise ValueError("Dados da transferência inválidos")

    campos_obrigatorios = ("valor", "conta_origem", "conta_destino")
    if any(campo not in transferencia for campo in campos_obrigatorios):
        raise ValueError("Dados da transferência inválidos")

    conta_origem = transferencia["conta_origem"]
    conta_destino = transferencia["conta_destino"]

    if not isinstance(conta_origem, dict) or not isinstance(conta_destino, dict):
        raise ValueError("Dados da transferência inválidos")

    subcampos_origem = ("numero", "tipo", "saldo")
    if any(campo not in conta_origem for campo in subcampos_origem):
        raise ValueError("Dados da transferência inválidos")

    if "numero" not in conta_destino:
        raise ValueError("Dados da transferência inválidos")

    valor = transferencia["valor"]
    tipo = conta_origem["tipo"]
    saldo = conta_origem["saldo"]

    def recusar(motivo):
        return {"status": "Recusada", "motivo": motivo}

    # Regra 2: tipos aceites
    if tipo not in LIMITES_TRANSFERENCIA:
        return recusar("Tipo de conta inválido")

    # Regra 3: contas diferentes
    if conta_origem["numero"] == conta_destino["numero"]:
        return recusar("Contas de origem e destino devem ser diferentes")

    # Regra 4: valor positivo
    if not valor > 0:
        return recusar("Valor da transferência deve ser maior que zero")

    # Regra 5: saldo suficiente
    if valor > saldo:
        return recusar("Saldo insuficiente")

    # Regra 6: limite por transferência (valor igual ao limite é permitido)
    if valor > LIMITES_TRANSFERENCIA[tipo]:
        return recusar("Limite de transferência excedido")

    # Regra 7: aprovação
    return {"status": "Aprovada", "motivo": "Transferência autorizada"}
