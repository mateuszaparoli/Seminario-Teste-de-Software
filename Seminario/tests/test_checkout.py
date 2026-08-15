"""
test_checkout.py - Demonstração do Plugin 'pytest-mock'.

O plugin 'pytest-mock' fornece a fixture 'mocker', uma camada fina e segura sobre unittest.mock:
- Não requer decorators complexos (@mock.patch) que poluem a assinatura da função.
- Desfaz todos os mocks automaticamente no teardown do teste (evita vazamento de estado entre testes).
- Fornece utilitários para mockar métodos, objetos, spies e stubs de forma limpa e idiomática.
"""
import pytest
from src.ecommerce.models import CarrinhoDeCompras, StatusPedido, Cliente
from src.ecommerce.checkout import ProcessadorCheckout, ReciboCheckout
from src.ecommerce.payment_service import (
    GatewayDePagamento,
    RespostaPagamento,
    CartaoRecusadoException,
    GatewayTimeoutException
)
from src.ecommerce.notification_service import ServicoNotificacao


class TestProcessadorCheckoutComMocks:
    """Testes de fluxo de checkout utilizando pytest-mock (fixture mocker)."""

    def test_checkout_sucesso_com_mock_gateway_e_spy_notificador(
        self,
        carrinho_com_produtos: CarrinhoDeCompras,
        mocker
    ):
        """
        Cenário: Pagamento aprovado com sucesso.
        Demonstra:
        - mocker.patch.object: substitui o método processar_cobranca para não chamar API real
        - mocker.spy: espiona o método enviar_email_confirmacao para checar se foi chamado
        """
        # 1. Instanciar serviços
        gateway = GatewayDePagamento()
        notificador = ServicoNotificacao()

        # 2. Configurar MOCK do gateway retornando resposta de sucesso pré-definida
        mock_processar = mocker.patch.object(
            gateway,
            "processar_cobranca",
            return_value=RespostaPagamento(
                sucesso=True,
                transacao_id="TX_MOCK_12345",
                mensagem="Pagamento aprovado no mock.",
                codigo_autorizacao="AUTH_MOCK"
            )
        )

        # 3. Configurar SPY no notificador para verificar chamada sem alterar seu comportamento
        spy_email = mocker.spy(notificador, "enviar_email_confirmacao")

        # 4. Executar Checkout
        processador = ProcessadorCheckout(gateway_pagamento=gateway, servico_notificacao=notificador)
        recibo = processador.processar(
            carrinho=carrinho_com_produtos,
            numero_cartao="1234567812345678",
            cvv="123",
            validade="12/28"
        )

        # 5. Asserções do Recibo
        assert isinstance(recibo, ReciboCheckout)
        assert recibo.status == StatusPedido.PAGO
        assert recibo.valor_total == 730.00
        assert recibo.transacao_id == "TX_MOCK_12345"

        # 6. Asserções do Mock (Verificar que o gateway foi invocado com os argumentos exatos)
        mock_processar.assert_called_once_with(
            cliente_id="CLI-1001",
            valor=730.00,
            numero_cartao="1234567812345678",
            cvv="123",
            validade="12/28"
        )

        # 7. Asserções do Spy (Verificar que o email foi enviado exatamente 1 vez com os dados certos)
        assert spy_email.call_count == 1
        args, kwargs = spy_email.call_args
        assert kwargs["email"] == "mateus@dcc.ufmg.br"
        assert kwargs["valor"] == 730.00

    def test_checkout_cartao_recusado_nao_envia_email(
        self,
        carrinho_com_produtos: CarrinhoDeCompras,
        mocker
    ):
        """
        Cenário: Gateway lança exceção de cartão recusado.
        Verifica se o checkout captura a falha e NÃO envia e-mail de confirmação.
        """
        gateway = GatewayDePagamento()
        notificador = ServicoNotificacao()

        # Simula lançamento de exceção pelo Gateway
        mocker.patch.object(
            gateway,
            "processar_cobranca",
            side_effect=CartaoRecusadoException("Limite indisponível.")
        )

        spy_email = mocker.spy(notificador, "enviar_email_confirmacao")

        processador = ProcessadorCheckout(gateway_pagamento=gateway, servico_notificacao=notificador)
        recibo = processador.processar(
            carrinho=carrinho_com_produtos,
            numero_cartao="1234567812349999",
            cvv="999",
            validade="05/27"
        )

        assert recibo.status == StatusPedido.FALHA_PAGAMENTO
        assert "Limite indisponível" in recibo.mensagem
        # E-mail de confirmação NUNCA deve ser disparado em caso de recusa!
        spy_email.assert_not_called()

    def test_checkout_gateway_timeout_deixa_pedido_pendente(
        self,
        carrinho_com_produtos: CarrinhoDeCompras,
        mocker
    ):
        """
        Cenário: Gateway sofre timeout. O status do pedido deve ficar PENDENTE para reprocessamento.
        """
        gateway = GatewayDePagamento()
        mocker.patch.object(
            gateway,
            "processar_cobranca",
            side_effect=GatewayTimeoutException("Timeout na API externa.")
        )

        processador = ProcessadorCheckout(gateway_pagamento=gateway)
        recibo = processador.processar(
            carrinho=carrinho_com_produtos,
            numero_cartao="1234567812340000",
            cvv="000",
            validade="01/29"
        )

        assert recibo.status == StatusPedido.PENDENTE
        assert "Indisponibilidade momentânea" in recibo.mensagem

    def test_checkout_carrinho_vazio_lanca_excecao(self, cliente_valido: Cliente):
        """Verifica que carrinho vazio não prossegue para cobrança."""
        carrinho_vazio = CarrinhoDeCompras(cliente=cliente_valido)
        processador = ProcessadorCheckout()

        with pytest.raises(ValueError, match="carrinho vazio"):
            processador.processar(
                carrinho=carrinho_vazio,
                numero_cartao="1234567812345678",
                cvv="123",
                validade="12/28"
            )
