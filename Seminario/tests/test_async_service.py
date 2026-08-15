"""
test_async_service.py - Demonstração do Plugin 'pytest-asyncio'.

O plugin 'pytest-asyncio' permite testar funções assíncronas (corrotinas async def com await)
de maneira totalmente transparente usando o decorator @pytest.mark.asyncio.
"""
import pytest
from src.ecommerce.notification_service import ServicoNotificacao


class TestServicoNotificacaoAsync:
    """Testes assíncronos para o serviço de notificações."""

    @pytest.mark.asyncio
    async def test_enviar_notificacao_push_async_sucesso(self):
        """Testa a execução de corrotina com await."""
        notificador = ServicoNotificacao()
        
        resultado = await notificador.enviar_notificacao_push_async(
            usuario_id="USR-456",
            titulo="Seu pedido foi faturado!",
            corpo="O pedido #PED-1234 já está sendo preparado."
        )

        assert resultado["status"] == "delivered"
        assert resultado["usuario_id"] == "USR-456"
        assert resultado["titulo"] == "Seu pedido foi faturado!"

    @pytest.mark.asyncio
    async def test_enviar_push_sem_usuario_lanca_erro(self):
        notificador = ServicoNotificacao()
        
        with pytest.raises(ValueError, match="ID de usuário obrigatório"):
            await notificador.enviar_notificacao_push_async(
                usuario_id="",
                titulo="Alerta",
                corpo="Mensagem teste"
            )
