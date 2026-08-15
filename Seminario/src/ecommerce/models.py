"""Modelos de domínio para itens, clientes e carrinho de compras."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from src.utils.validators import calcular_desconto_cupom, validar_cpf, validar_email


class StatusPedido(Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    FALHA_PAGAMENTO = "falha_pagamento"
    CANCELADO = "cancelado"
    ENVIADO = "enviado"


@dataclass
class Item:
    nome: str
    preco_unitario: float
    quantidade: int = 1

    def __post_init__(self):
        if self.preco_unitario < 0:
            raise ValueError(f"Preço unitário não pode ser negativo: {self.preco_unitario}")
        if self.quantidade <= 0:
            raise ValueError(f"Quantidade deve ser maior que zero: {self.quantidade}")

    @property
    def subtotal(self) -> float:
        return round(self.preco_unitario * self.quantidade, 2)


@dataclass
class Cliente:
    id: str
    nome: str
    email: str
    cpf: str
    eh_vip: bool = False

    def __post_init__(self):
        if not validar_email(self.email):
            raise ValueError(f"E-mail inválido fornecido: {self.email}")
        if not validar_cpf(self.cpf):
            raise ValueError(f"CPF inválido fornecido: {self.cpf}")


@dataclass
class CarrinhoDeCompras:
    cliente: Cliente
    itens: List[Item] = field(default_factory=list)
    cupom: Optional[str] = None

    def adicionar_item(self, item: Item) -> None:
        """Adiciona um item ao carrinho ou incrementa quantidade se já existir."""
        for item_existente in self.itens:
            if item_existente.nome == item.nome and item_existente.preco_unitario == item.preco_unitario:
                item_existente.quantidade += item.quantidade
                return
        self.itens.append(item)

    def remover_item(self, nome_item: str) -> bool:
        """Remove item pelo nome. Retorna True se encontrado e removido."""
        for i, item in enumerate(self.itens):
            if item.nome == nome_item:
                self.itens.pop(i)
                return True
        return False

    def aplicar_cupom(self, cupom: str) -> None:
        """Valida e aplica cupom de desconto ao carrinho."""
        # Testa validação de cupom com subtotal atual
        calcular_desconto_cupom(cupom, self.subtotal)
        self.cupom = cupom

    @property
    def subtotal(self) -> float:
        return round(sum(item.subtotal for item in self.itens), 2)

    @property
    def desconto(self) -> float:
        desconto_cupom = calcular_desconto_cupom(self.cupom, self.subtotal)
        # Desconto adicional de 5% se o cliente for VIP
        if self.cliente.eh_vip:
            desconto_vip = round(self.subtotal * 0.05, 2)
            return min(desconto_cupom + desconto_vip, self.subtotal)
        return min(desconto_cupom, self.subtotal)

    @property
    def total(self) -> float:
        return round(max(0.0, self.subtotal - self.desconto), 2)

    @property
    def esta_vazio(self) -> bool:
        return len(self.itens) == 0
