"""
Arquivo conftest.py - Fixtures Globais do Pytest.

Conceitos Fundamentais Demonstrados Aqui:
1. Descoberta Automática: O Pytest carrega conftest.py automaticamente (não precisa importar nos testes).
2. Injeção de Dependência: Fixtures podem receber outras fixtures como parâmetros.
3. Escopos (Scopes): function, class, module, package, session.
4. Setup e Teardown com yield: Código antes do yield é setup; código após o yield é teardown.
"""
import pytest
from src.ecommerce.models import Cliente, Item, CarrinhoDeCompras


@pytest.fixture(scope="session", autouse=True)
def sessao_de_testes_info():
    """
    Fixture com escopo de 'session' e 'autouse=True'.
    Executa uma única vez no início de toda a suíte de testes e faz limpeza no final.
    """
    print("\n🚀 [SETUP SESSION] Iniciando suíte de testes do Seminário Pytest...")
    yield
    print("\n🏁 [TEARDOWN SESSION] Suíte de testes finalizada com sucesso!")


@pytest.fixture
def cliente_valido() -> Cliente:
    """Fixture básica que provê um cliente padrão válido (não VIP)."""
    return Cliente(
        id="CLI-1001",
        nome="Mateus Zaparoli",
        email="mateus@dcc.ufmg.br",
        cpf="111.444.777-35",  # CPF com algoritmo de validação válido
        eh_vip=False
    )


@pytest.fixture
def cliente_vip() -> Cliente:
    """Fixture que provê um cliente VIP (recebe 5% de desconto extra)."""
    return Cliente(
        id="CLI-VIP-777",
        nome="Ana Silva",
        email="ana.silva@ufmg.br",
        cpf="529.982.247-25",  # CPF com algoritmo válido
        eh_vip=True
    )


@pytest.fixture
def itens_padrao() -> list[Item]:
    """Retorna uma lista de itens de teste."""
    return [
        Item(nome="Teclado Mecânico Keychron", preco_unitario=350.0, quantidade=1),
        Item(nome="Mouse Ergonômico Logitech", preco_unitario=150.0, quantidade=2),
        Item(nome="Mousepad Deskmat", preco_unitario=80.0, quantidade=1)
    ]


@pytest.fixture
def carrinho_com_produtos(cliente_valido: Cliente, itens_padrao: list[Item]) -> CarrinhoDeCompras:
    """
    DEMONSTRAÇÃO DE COMPOSIÇÃO DE FIXTURES (Dependency Injection):
    Esta fixture depende de 'cliente_valido' e 'itens_padrao'.
    O Pytest resolve a árvore de dependências automaticamente.
    Subtotal inicial esperado: 350 + (150*2) + 80 = 730.00
    """
    carrinho = CarrinhoDeCompras(cliente=cliente_valido)
    for item in itens_padrao:
        carrinho.adicionar_item(item)
    return carrinho


@pytest.fixture
def carrinho_vip_com_produtos(cliente_vip: Cliente, itens_padrao: list[Item]) -> CarrinhoDeCompras:
    """Carrinho com cliente VIP para testes de regras de desconto cumulativas."""
    carrinho = CarrinhoDeCompras(cliente=cliente_vip)
    for item in itens_padrao:
        carrinho.adicionar_item(item)
    return carrinho


@pytest.fixture
def recurso_temporario_com_teardown():
    """
    DEMONSTRAÇÃO DE SETUP E TEARDOWN COM YIELD:
    Útil para bancos de dados em memória, arquivos temporários, conexões mockadas, etc.
    """
    recurso = {"status": "conectado", "dados": [1, 2, 3]}
    print("\n  [SETUP] Recurso temporário alocado.")
    
    yield recurso  # Aqui o teste executa e consome o recurso
    
    # Após o teste terminar, o fluxo continua aqui (Teardown garantido mesmo se o teste falhar)
    recurso["status"] = "desconectado"
    recurso["dados"].clear()
    print("  [TEARDOWN] Recurso temporário desalocado com segurança.")
