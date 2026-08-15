"""
test_models.py - Demonstração de Fixtures, Injeção de Dependência e Exceções.
"""
import pytest
from src.ecommerce.models import Item, Cliente, CarrinhoDeCompras


class TestItemModel:
    """Testes de unidade para o modelo Item."""

    def test_criacao_item_valido(self):
        item = Item(nome="Monitor 4K 27''", preco_unitario=1800.0, quantidade=2)
        assert item.nome == "Monitor 4K 27''"
        assert item.preco_unitario == 1800.0
        assert item.quantidade == 2
        assert item.subtotal == 3600.0

    def test_item_com_preco_negativo_lanca_excecao(self):
        with pytest.raises(ValueError, match="Preço unitário não pode ser negativo"):
            Item(nome="Produto Inválido", preco_unitario=-10.0, quantidade=1)

    def test_item_com_quantidade_invalida_lanca_excecao(self):
        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            Item(nome="Produto Zero", preco_unitario=50.0, quantidade=0)


class TestClienteModel:
    """Testes para o modelo Cliente utilizando fixtures."""

    def test_cliente_valido(self, cliente_valido: Cliente):
        """Usa fixture 'cliente_valido' injetada automaticamente."""
        assert cliente_valido.id == "CLI-1001"
        assert cliente_valido.nome == "Mateus Zaparoli"
        assert cliente_valido.eh_vip is False

    def test_cliente_com_email_invalido_lanca_erro(self):
        with pytest.raises(ValueError, match="E-mail inválido"):
            Cliente(
                id="CLI-ERR",
                nome="Fulano",
                email="email_invalido_sem_arroba",
                cpf="111.444.777-35"
            )

    def test_cliente_com_cpf_invalido_lanca_erro(self):
        with pytest.raises(ValueError, match="CPF inválido"):
            Cliente(
                id="CLI-ERR",
                nome="Fulano",
                email="fulano@ufmg.br",
                cpf="111.111.111-11"
            )


class TestCarrinhoDeCompras:
    """Testes de lógica de negócio do carrinho utilizando fixtures compostas."""

    def test_carrinho_inicialmente_calcula_subtotal_correto(
        self,
        carrinho_com_produtos: CarrinhoDeCompras
    ):
        """
        Itens:
        - Teclado (1x 350.0) = 350.0
        - Mouse (2x 150.0) = 300.0
        - Mousepad (1x 80.0) = 80.0
        Subtotal esperado: 730.00
        """
        assert carrinho_com_produtos.subtotal == 730.00
        assert carrinho_com_produtos.desconto == 0.0
        assert carrinho_com_produtos.total == 730.00
        assert not carrinho_com_produtos.esta_vazio

    def test_adicionar_item_duplicado_incrementa_quantidade(
        self,
        carrinho_com_produtos: CarrinhoDeCompras
    ):
        # Adiciona outro Teclado Mecânico (mesmo nome e preço)
        novo_teclado = Item(nome="Teclado Mecânico Keychron", preco_unitario=350.0, quantidade=2)
        carrinho_com_produtos.adicionar_item(novo_teclado)

        assert len(carrinho_com_produtos.itens) == 3  # Não cria nova linha na lista
        item_teclado = next(i for i in carrinho_com_produtos.itens if i.nome == "Teclado Mecânico Keychron")
        assert item_teclado.quantidade == 3
        assert carrinho_com_produtos.subtotal == 1430.00

    def test_remover_item_existente(self, carrinho_com_produtos: CarrinhoDeCompras):
        removido = carrinho_com_produtos.remover_item("Mousepad Deskmat")
        assert removido is True
        assert len(carrinho_com_produtos.itens) == 2
        assert carrinho_com_produtos.subtotal == 650.00

    def test_remover_item_inexistente_retorna_false(self, carrinho_com_produtos: CarrinhoDeCompras):
        removido = carrinho_com_produtos.remover_item("Item Fantasma")
        assert removido is False
        assert len(carrinho_com_produtos.itens) == 3

    def test_carrinho_com_cupom_desc10(self, carrinho_com_produtos: CarrinhoDeCompras):
        carrinho_com_produtos.aplicar_cupom("DESC10")
        assert carrinho_com_produtos.subtotal == 730.00
        assert carrinho_com_produtos.desconto == 73.00
        assert carrinho_com_produtos.total == 657.00

    def test_carrinho_cliente_vip_com_cupom(self, carrinho_vip_com_produtos: CarrinhoDeCompras):
        """
        Cliente VIP ganha +5% de desconto acumulado com o cupom.
        Subtotal: 730.00
        Cupom DESC10: 10% de 730 = 73.00
        Desconto VIP: 5% de 730 = 36.50
        Total desconto: 109.50
        Total final: 620.50
        """
        carrinho_vip_com_produtos.aplicar_cupom("DESC10")
        assert carrinho_vip_com_produtos.desconto == 109.50
        assert carrinho_vip_com_produtos.total == 620.50

    def test_fixture_com_teardown(self, recurso_temporario_com_teardown):
        """Demonstra consumo de fixture com setup e teardown garantido."""
        assert recurso_temporario_com_teardown["status"] == "conectado"
        assert len(recurso_temporario_com_teardown["dados"]) == 3
