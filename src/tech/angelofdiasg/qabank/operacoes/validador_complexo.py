def validar_cliente_premium(cliente):
    """
    Função que valida se um cliente (objeto/dicionário) tem os 
    requisitos para ter um Cartão de Crédito Premium.
    
    Regras de Negócio:
    1. Idade >= 18 anos.
    2. Morada deve ter um código postal ('cep') válido (não vazio).
    3. Histórico de crédito (score) > 700.
    4. Renda mensal >= 5000.
    """
    if not cliente or not isinstance(cliente, dict):
        raise ValueError("Dados do cliente inválidos ou ausentes.")

    # 1. Valida Idade
    if cliente.get("idade", 0) < 18:
        return {"status": "Recusado", "motivo": "Idade inferior a 18 anos"}

    # 2. Valida Morada
    morada = cliente.get("morada", {})
    if not morada.get("cep") or len(morada.get("cep", "")) < 5:
        return {"status": "Recusado", "motivo": "Código postal inválido"}

    # 3. Valida Score
    financeiro = cliente.get("dados_financeiros", {})
    if financeiro.get("score_credito", 0) <= 700:
        return {"status": "Recusado", "motivo": "Score de crédito insuficiente"}

    # 4. Valida Renda
    if financeiro.get("renda_mensal", 0) < 5000:
        return {"status": "Recusado", "motivo": "Renda mensal insuficiente"}

    return {"status": "Aprovado", "motivo": "Cliente elegível para Cartão Premium"}