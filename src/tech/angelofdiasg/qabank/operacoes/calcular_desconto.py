def calcular_desconto(valor_compra):
    """
    Calcula o valor com desconto com base no valor da compra.
    - Até 100: 0% desconto
    - 101 a 500: 10% desconto
    - Acima de 500: 20% desconto
    """
    if valor_compra < 0:
        raise ValueError("Valor da compra não pode ser negativo")
        
    if valor_compra <= 100:
        return valor_compra
    elif valor_compra <= 500:
        desconto = valor_compra * 0.10
        return valor_compra - desconto
    else:
        desconto = valor_compra * 0.20
        return valor_compra - desconto