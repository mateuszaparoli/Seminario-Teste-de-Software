"""Validações e regras de negócio para entradas de dados."""
import re
from typing import Optional


def validar_cpf(cpf: str) -> bool:
    """
    Valida se um CPF é válido segundo o algoritmo de dígitos verificadores da Receita Federal.
    Aceita CPFs formatados (ex: '123.456.789-00') ou apenas dígitos.
    """
    if not isinstance(cpf, str):
        return False

    # Remove pontuação
    digitos = [int(c) for c in cpf if c.isdigit()]

    if len(digitos) != 11:
        return False

    # Rejeita sequências de dígitos iguais (ex: '11111111111')
    if len(set(digitos)) == 1:
        return False

    # Primeiro dígito verificador
    soma = sum(a * b for a, b in zip(digitos[:9], range(10, 1, -1)))
    resto = (soma * 10) % 11
    d1 = 0 if resto == 10 else resto
    if d1 != digitos[9]:
        return False

    # Segundo dígito verificador
    soma = sum(a * b for a, b in zip(digitos[:10], range(11, 1, -1)))
    resto = (soma * 10) % 11
    d2 = 0 if resto == 10 else resto
    if d2 != digitos[10]:
        return False

    return True


def validar_email(email: str) -> bool:
    """Valida formato básico de email usando regex."""
    if not isinstance(email, str) or not email.strip():
        return False
    
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(padrao, email.strip()))


def calcular_desconto_cupom(cupom: Optional[str], valor_subtotal: float) -> float:
    """
    Calcula o valor do desconto a ser aplicado baseado no cupom.
    Retorna o valor absoluto do desconto em reais.
    
    Regras:
    - 'DESC10': 10% de desconto
    - 'DESC20': 20% de desconto para compras acima de R$ 100
    - 'FRETEGRATIS': Desconto fixo de R$ 15 para compras acima de R$ 50
    - 'VIP50': 50% de desconto até um teto máximo de R$ 100 de desconto
    """
    if not cupom or not isinstance(cupom, str):
        return 0.0

    cupom_normalizado = cupom.strip().upper()
    
    if valor_subtotal <= 0:
        return 0.0

    if cupom_normalizado == "DESC10":
        return round(valor_subtotal * 0.10, 2)

    elif cupom_normalizado == "DESC20":
        if valor_subtotal >= 100.0:
            return round(valor_subtotal * 0.20, 2)
        return 0.0

    elif cupom_normalizado == "FRETEGRATIS":
        if valor_subtotal >= 50.0:
            return min(15.0, valor_subtotal)
        return 0.0

    elif cupom_normalizado == "VIP50":
        desconto = valor_subtotal * 0.50
        return round(min(desconto, 100.0), 2)

    raise ValueError(f"Cupom inválido ou expirado: '{cupom}'")
