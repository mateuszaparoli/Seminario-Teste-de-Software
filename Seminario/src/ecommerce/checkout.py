"""Orquestrador do processo de Checkout de compras."""
from dataclasses import dataclass
from typing import Optional
import uuid

from src.ecommerce.models import CarrinhoDeCompras, StatusPedido
from src.ecommerce.payment_service import (
    GatewayDePagamento,
    CartaoRecusadoException,
    GatewayTimeoutException,
    GatewayException
)
from src.ecommerce.notification_service import ServicoNotificacao


@dataclass
class ReciboCheckout:
    pedido_id: str
    cliente_nome: str
    valor_total: float
    desconto_aplicado: float
    status: StatusPedido
    mensagem: str
    transacao_id: Optional[str] = None


class ProcessadorCheckout:
    def __init__(
        self,
        gateway_pagamento: Optional[GatewayDePagamento] = None,
        servico_notificacao: Optional[ServicoNotificacao] = None
    ):
        self.gateway = gateway_pagamento or GatewayDePagamento()
        self.notificador = servico_notificacao or ServicoNotificacao()

    def processar(
        self,
        carrinho: CarrinhoDeCompras,
        numero_cartao: str,
        cvv: str,
        validade: str
    ) -> ReciboCheckout:
        """
        Executa todo o fluxo de fechamento do pedido:
        1. Validação do carrinho
        2. Processamento do pagamento no gateway
        3. Envio de notificações
        4. Retorno do recibo consolidado
        """
        if carrinho.esta_vazio:
            raise ValueError("Não é possível realizar checkout com carrinho vazio.")

        valor_total = carrinho.total
        desconto = carrinho.desconto
        pedido_id = f"PED-{uuid.uuid4().hex[:8].upper()}"

        try:
            resposta_pagamento = self.gateway.processar_cobranca(
                cliente_id=carrinho.cliente.id,
                valor=valor_total,
                numero_cartao=numero_cartao,
                cvv=cvv,
                validade=validade
            )

            # Notificar cliente após confirmação
            self.notificador.enviar_email_confirmacao(
                email=carrinho.cliente.email,
                pedido_id=pedido_id,
                valor=valor_total
            )

            return ReciboCheckout(
                pedido_id=pedido_id,
                cliente_nome=carrinho.cliente.nome,
                valor_total=valor_total,
                desconto_aplicado=desconto,
                status=StatusPedido.PAGO,
                mensagem=resposta_pagamento.mensagem,
                transacao_id=resposta_pagamento.transacao_id
            )

        except CartaoRecusadoException as e:
            return ReciboCheckout(
                pedido_id=pedido_id,
                cliente_nome=carrinho.cliente.nome,
                valor_total=valor_total,
                desconto_aplicado=desconto,
                status=StatusPedido.FALHA_PAGAMENTO,
                mensagem=f"Falha de pagamento: {str(e)}"
            )

        except (GatewayTimeoutException, GatewayException) as e:
            return ReciboCheckout(
                pedido_id=pedido_id,
                cliente_nome=carrinho.cliente.nome,
                valor_total=valor_total,
                desconto_aplicado=desconto,
                status=StatusPedido.PENDENTE,
                mensagem=f"Indisponibilidade momentânea: {str(e)}"
            )
