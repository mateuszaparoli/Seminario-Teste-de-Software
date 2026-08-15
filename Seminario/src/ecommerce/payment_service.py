"""Serviço simulado de comunicação com Gateway de Pagamento externo."""
from dataclasses import dataclass
import time
from typing import Dict, Any


class GatewayException(Exception):
    """Exceção base para problemas no gateway."""
    pass


class CartaoRecusadoException(GatewayException):
    """Lançada quando a operadora de cartão recusa a transação."""
    pass


class GatewayTimeoutException(GatewayException):
    """Lançada quando a API do gateway de pagamento não responde a tempo."""
    pass


@dataclass
class RespostaPagamento:
    sucesso: bool
    transacao_id: str
    mensagem: str
    codigo_autorizacao: str


class GatewayDePagamento:
    """
    Simula uma integração real com provedores como Stripe, Pagar.me ou MercadoPago.
    Em testes unitários, métodos desta classe devem ser MOCKADOS com pytest-mock!
    """

    def processar_cobranca(
        self,
        cliente_id: str,
        valor: float,
        numero_cartao: str,
        cvv: str,
        validade: str
    ) -> RespostaPagamento:
        """
        Em produção, faria uma chamada HTTP POST para a API externa.
        Aqui simula atraso de rede e regras de validação.
        """
        if valor <= 0:
            raise ValueError(f"Valor para cobrança deve ser positivo: {valor}")

        if not numero_cartao or len(numero_cartao.replace(" ", "")) != 16:
            raise CartaoRecusadoException("Número de cartão inválido.")

        # Simulação de latência de rede externa
        time.sleep(0.05)

        # Regra de simulação: cartões terminados em 0000 simulam erro de timeout
        if numero_cartao.endswith("0000"):
            raise GatewayTimeoutException("Timeout na comunicação com a adquirente.")

        # Regra de simulação: cartões terminados em 9999 simulam recusa de limite
        if numero_cartao.endswith("9999"):
            raise CartaoRecusadoException("Transação negada pela emissora do cartão (Saldo insuficiente).")

        return RespostaPagamento(
            sucesso=True,
            transacao_id=f"tx_{int(time.time()*1000)}_{cliente_id[:4]}",
            mensagem="Pagamento aprovado com sucesso.",
            codigo_autorizacao="AUTH_998877"
        )
