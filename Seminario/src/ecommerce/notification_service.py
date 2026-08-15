"""Serviço simulado de envio de notificações e e-mails."""
import asyncio
from typing import Dict, Any


class ServicoNotificacao:
    """Simulador de envio de notificações via Email, SMS e Push."""

    def enviar_email_confirmacao(self, email: str, pedido_id: str, valor: float) -> bool:
        """Envia e-mail de confirmação de pedido."""
        if not email or "@" not in email:
            raise ValueError(f"Email destinatário inválido: {email}")
        
        # Simula envio de email
        print(f"[EMAIL] Enviado para {email}: Pedido #{pedido_id} aprovado no valor de R${valor:.2f}")
        return True

    def enviar_sms_alerta(self, telefone: str, mensagem: str) -> bool:
        """Envia SMS de alerta."""
        if not telefone:
            return False
        print(f"[SMS] Enviado para {telefone}: {mensagem}")
        return True

    async def enviar_notificacao_push_async(self, usuario_id: str, titulo: str, corpo: str) -> Dict[str, Any]:
        """
        Envia push notification de forma assíncrona.
        Excelente para demonstrar o plugin `pytest-asyncio`!
        """
        if not usuario_id:
            raise ValueError("ID de usuário obrigatório para envio de Push.")
        
        # Simula latência de rede assíncrona
        await asyncio.sleep(0.01)
        
        return {
            "status": "delivered",
            "usuario_id": usuario_id,
            "titulo": titulo,
            "corpo": corpo
        }
