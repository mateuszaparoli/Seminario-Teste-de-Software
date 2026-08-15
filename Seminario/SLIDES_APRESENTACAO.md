---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #f5f7fa
color: #1e293b
style: |
  section {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 24px;
    padding: 40px 60px;
  }
  h1 {
    color: #0284c7;
    font-size: 42px;
  }
  h2 {
    color: #0369a1;
    font-size: 32px;
  }
  pre {
    background-color: #1e293b;
    color: #f8fafc;
    border-radius: 8px;
    padding: 16px;
    font-size: 18px;
  }
  footer {
    font-size: 14px;
    color: #64748b;
  }
---

# Pytest e seu Ecossistema de Plugins
### Da Teoria à Prática no Desenvolvimento Moderno

**Disciplina:** Teste de Software (DCC / UFMG)  
**Apresentador:** Mateus Zaparoli  

---

## 🎯 Objetivos do Seminário

- Compreender a evolução dos frameworks de teste em Python (Unittest vs. Pytest).
- Dominar os pilares nativos do Pytest:
  - Asserções nativas com reescrita de AST (*AST Rewriting*)
  - Injeção de Dependências com **Fixtures**
  - Testes baseados em dados com **`@pytest.mark.parametrize`**
- Explorar o poderoso ecossistema de **Plugins**:
  - `pytest-cov`, `pytest-mock`, `pytest-xdist`, `pytest-sugar`, `pytest-html`, `pytest-asyncio`
- **Demonstração Prática ao Vivo** de uma suíte real de E-Commerce.

---

## ⚖️ O Cenário: Unittest vs. Pytest

| Característica | Python `unittest` (Standard) | `Pytest` |
| :--- | :--- | :--- |
| **Paradigma** | Orientado a Objetos rígido (xUnit / JUnit) | Baseado em funções puras ou classes simples |
| **Asserções** | Dezenas de métodos (`self.assertEqual`, etc.) | Declaração nativa `assert a == b` |
| **Gerenciamento de Estado** | `setUp()` e `tearDown()` com escopo fixo | **Fixtures** modulares e injetáveis por escopo |
| **Parametrização** | Difícil (requer `subTest` ou libs externas) | Nativa com `@pytest.mark.parametrize` |
| **Extensibilidade** | Limitada | Arquitetura aberta via **Pluggy** (> 1000 plugins) |

---

## ⚡ O Superpoder das Asserções Simples: AST Rewriting

No Pytest, você usa apenas o `assert` padrão do Python:

```python
def test_calculo_total():
    carrinho = Carrinho()
    carrinho.adicionar(Item("Mouse", 150.0))
    assert carrinho.total == 200.0  # Erro intencional
```

**O que o Pytest faz por baixo dos panos?**
- Durante a importação dos testes, o Pytest intercepta a Árvore Sintática Abstrata (AST).
- Se a asserção falhar, ele decompõe cada subexpressão:
  ```text
  AssertionError: assert 150.0 == 200.0
   +  where 150.0 = <Carrinho com 1 item>.total
  ```
- **Zero necessidade de aprender dezenas de `self.assertXYZ`!**

---

## 💉 Fixtures: Injeção de Dependência Elegante

Fixtures fornecem dados, conexões e estados para testes de forma explícita e modular.

```python
# conftest.py
@pytest.fixture
def cliente_padrao():
    return Cliente(id="CLI-1", nome="Mateus", email="mateus@ufmg.br")

@pytest.fixture
def carrinho_pronto(cliente_padrao):  # Composição de fixtures!
    carrinho = CarrinhoDeCompras(cliente=cliente_padrao)
    carrinho.adicionar_item(Item("Teclado", 350.0))
    return carrinho
```

```python
# test_carrinho.py
def test_desconto_carrinho(carrinho_pronto):
    carrinho_pronto.aplicar_cupom("DESC10")
    assert carrinho_pronto.total == 315.0
```

---

## 🔄 Ciclo de Vida e Teardown com `yield`

Como gerenciar recursos com segurança (banco de dados, arquivos temporários, conexões)?

```python
@pytest.fixture(scope="module")
def banco_dados_teste():
    # SETUP
    db = inicializar_banco_em_memoria()
    popular_tabelas(db)
    
    yield db  # Ponto em que os testes são executados
    
    # TEARDOWN (Garantido mesmo se os testes falharem)
    db.limpar_tudo()
    db.desconectar()
```

- **Escopos disponíveis:** `function` (padrão), `class`, `module`, `package`, `session`.

---

## 📊 Parametrização: Testes Baseados em Dados

Elimine duplicação testando dezenas de casos de borda com uma única função:

```python
@pytest.mark.parametrize(
    "cupom, subtotal, desconto_esperado",
    [
        ("DESC10", 100.0, 10.0),
        ("DESC20", 200.0, 40.0),
        ("DESC20", 90.0, 0.0),      # Não atinge valor mínimo
        ("FRETEGRATIS", 60.0, 15.0),
        (None, 100.0, 0.0),
    ],
    ids=["desc10_padrao", "desc20_valido", "desc20_invalido", "frete_gratis", "sem_cupom"]
)
def test_calculo_descontos(cupom, subtotal, desconto_esperado):
    assert calcular_desconto_cupom(cupom, subtotal) == desconto_esperado
```

---

## 🧩 O Ecossistema de Plugins do Pytest

O Pytest é construído sobre o **Pluggy** (gerenciador de ganchos / *hook architecture*).

Tudo no Pytest — desde a coleta de arquivos até a geração de relatórios — passa por ganchos (`pytest_runtest_protocol`, `pytest_collect_file`, etc.).

### Plugins Essenciais no Mercado:
1. **Qualidade & Métricas:** `pytest-cov`, `pytest-benchmark`
2. **Isolamento & Test Doubles:** `pytest-mock`, `pytest-responses`, `freezegun`
3. **Desempenho & Escala:** `pytest-xdist`, `pytest-picked`
4. **Experiência & Relatórios:** `pytest-sugar`, `pytest-html`, `allure-pytest`
5. **Assíncrono & Web:** `pytest-asyncio`, `pytest-django`, `pytest-playwright`

---

## 🛡️ Plugin 1: `pytest-mock` (Isolamento sem Dor)

Por que usar `pytest-mock` em vez de `unittest.mock.patch` com decorators?

```python
def test_checkout_com_sucesso(carrinho_com_produtos, mocker):
    # 1. Mock limpo sem poluir decorators
    mock_gateway = mocker.patch("src.ecommerce.payment_service.GatewayDePagamento.processar_cobranca")
    mock_gateway.return_value = RespostaPagamento(sucesso=True, transacao_id="TX-99")

    # 2. Spy para inspecionar chamadas sem alterar o comportamento
    spy_notificador = mocker.spy(ServicoNotificacao, "enviar_email_confirmacao")

    processador = ProcessadorCheckout()
    recibo = processador.processar(carrinho_com_produtos, "1234567812345678", "123", "12/28")

    assert recibo.status == StatusPedido.PAGO
    spy_notificador.assert_called_once()
    # Teardown de todos os mocks ocorre AUTOMATICAMENTE!
```

---

## 🏎️ Plugin 2: `pytest-xdist` (Execução Paralela)

Em suítes grandes com centenas ou milhares de testes, o tempo de execução é gargalo.

- **Como funciona:** O `pytest-xdist` cria múltiplos *workers* (processos Python isolados) e distribui os testes entre os núcleos de CPU disponíveis.

```bash
# Executa utilizando todos os núcleos de CPU disponíveis:
pytest -n auto

# Executa fixando 4 processos de trabalho:
pytest -n 4
```

> **Resultado prático na demo:** 6 testes lentos caem de **~2.4 segundos** para **~0.45 segundos**!

---

## 📈 Plugin 3: `pytest-cov` (Cobertura de Código)

Mede exatamente quais linhas, ramificações (*branch coverage*) e módulos foram exercitados pelos testes.

```bash
# Exibe resumo no terminal com linhas faltantes e gera relatório HTML:
pytest --cov=src --cov-report=term-missing --cov-report=html
```

- Integração nativa com a ferramenta padrão `Coverage.py`.
- Permite definir metas mínimas de cobertura no CI/CD (`--cov-fail-under=90`).

---

## 🎨 Plugins Visuais: `pytest-sugar` & `pytest-html`

### `pytest-sugar`
- Substitui a saída estática de pontos (`....F...`) por uma **barra de progresso colorida e dinâmica**, com indicação instantânea de falhas.

### `pytest-html`
- Gera um relatório standalone em HTML com filtros, tempo de execução, metadados do ambiente e rastreamento de falhas:
```bash
pytest --html=reports/report.html --self-contained-html
```

---

## ⚡ Plugin 5: `pytest-asyncio` (Python Moderno)

Aplicações com FastAPI, aiohttp ou microserviços orientados a eventos dependem de corrotinas assíncronas (`async`/`await`).

```python
@pytest.mark.asyncio
async def test_envio_notificacao_push():
    notificador = ServicoNotificacao()
    resultado = await notificador.enviar_notificacao_push_async(
        usuario_id="USR-01",
        titulo="Pedido Enviado",
        corpo="Seu código de rastreio é BR123"
    )
    assert resultado["status"] == "delivered"
```

---

## 💻 Demonstração Prática (Live Demo)

### Domínio: Módulo de Checkout de E-Commerce
1. **Passo 1:** Execução geral com `pytest-sugar`.
2. **Passo 2:** Validação de CPF/Email com `@pytest.mark.parametrize` (10 casos de teste).
3. **Passo 3:** Mocking de Gateway de Pagamento com `pytest-mock` (Sucesso, Cartão Recusado, Timeout).
4. **Passo 4:** Comparação de performance sequencial vs. paralelo com `pytest-xdist` (`-n auto`).
5. **Passo 5:** Testes de corrotinas assíncronas com `pytest-asyncio`.
6. **Passo 6:** Medição de cobertura com `pytest-cov` e abertura do relatório `pytest-html`.

---

## 🏆 Melhores Práticas com Pytest

1. **Mantenha os testes independentes e determinísticos** (sem dependência de ordem).
2. **Use `conftest.py` com sabedoria:** Concentre fixtures reutilizáveis sem poluir arquivos de teste.
3. **Priorize `@pytest.mark.parametrize`** para classes de equivalência e análise de valor limite.
4. **Use `pytest.ini` ou `pyproject.toml`** para padronizar opções (`addopts`) e registrar `markers`.
5. **Evite over-mocking:** Mock apenas fronteiras externas de I/O (APIs de terceiros, gateways, filas).

---

## ❓ Perguntas & Discussão

- **Repositório do Projeto:** Disponível para consulta e reprodução.
- **Agradecimentos:** DCC / UFMG - Disciplina de Teste de Software.

**Obrigado!**
