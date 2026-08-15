# AGENTS.md - Diretrizes do Projeto de Seminário: Pytest e Plugins

Este repositório contém o material de estudo, apresentação e projeto prático de demonstração para o seminário da disciplina **Teste de Software (DCC/UFMG)** sobre o tema: **"Pytest e seus Plugins: Da Teoria à Prática"**.

---

## 🎯 Objetivo do Repositório

1. **Apresentação Teórica e Prática:** Estruturar uma apresentação clara, moderna e impactante sobre o ecossistema Pytest.
2. **Demonstração Prática:** Prover um projeto Python real (módulo de E-commerce/Checkout) com uma suíte de testes completa demonstrando os recursos nativos do Pytest e seus principais plugins.
3. **Material de Preparação:** Fornecer roteiro, guia de estudo aprofundado e comandos de demonstração para o apresentador.

---

## 📁 Estrutura do Workspace

```text
.
├── AGENTS.md                          # Este arquivo de governança para agentes e desenvolvedores
└── Seminario/
    ├── README.md                      # Instruções de execução rápida do projeto
    ├── GUIA_ESTUDO_PYTEST.md          # Guia técnico aprofundado, arquitetura e roteiro de fala
    ├── SLIDES_APRESENTACAO.md         # Estrutura completa dos slides em Markdown (compatível com Marp/Slidev)
    ├── requirements.txt               # Dependências do Pytest e Plugins selecionados
    ├── pytest.ini                     # Configuração padronizada do pytest (markers, flags, paths)
    ├── demo_script.sh                 # Script bash interativo para execução guiada da demo ao vivo
    ├── src/                           # Código fonte do domínio de negócio (E-commerce)
    │   ├── __init__.py
    │   ├── ecommerce/
    │   │   ├── __init__.py
    │   │   ├── models.py              # Modelos: Item, Carrinho, Cupom, Cliente
    │   │   ├── payment_service.py     # Gateway de pagamento simulado
    │   │   ├── notification_service.py# Serviço de notificações (síncrono e assíncrono)
    │   │   └── checkout.py            # Orquestrador de regras de negócio de checkout
    │   └── utils/
    │       ├── __init__.py
    │       └── validators.py          # Validadores (CPF, Email, Cupons) para testes parametrizados
    └── tests/                         # Suíte de testes automatizados
        ├── __init__.py
        ├── conftest.py                # Fixtures globais reutilizáveis
        ├── test_validators.py         # Demonstração: Asserções nativas e @pytest.mark.parametrize
        ├── test_models.py             # Demonstração: Fixtures, escopos e pytest.raises
        ├── test_checkout.py           # Demonstração: pytest-mock (mocker, spies e stubs)
        ├── test_performance_slow.py   # Demonstração: pytest-xdist (execução paralela) e markers
        └── test_async_service.py      # Demonstração: pytest-asyncio (testes assíncronos)
```

---

## 🛠️ Plugins Cobertos na Demonstração

| Plugin | Finalidade Principal | Comando de Demonstração |
| :--- | :--- | :--- |
| **`pytest-sugar`** | Visualização moderna no terminal com barra de progresso e cores | `pytest` |
| **`pytest-cov`** | Medição de cobertura de código (CLI e relatório HTML interativo) | `pytest --cov=src --cov-report=term-missing --cov-report=html` |
| **`pytest-mock`** | Integração limpa de mocks/stubs via fixture `mocker` | `pytest tests/test_checkout.py -v` |
| **`pytest-xdist`** | Execução paralela de testes distribuída por núcleos de CPU | `pytest tests/test_performance_slow.py -n auto` |
| **`pytest-html`** | Geração de relatório HTML standalone completo para auditoria | `pytest --html=reports/report.html --self-contained-html` |
| **`pytest-asyncio`** | Suporte nativo a corrotinas e código assíncrono (`async`/`await`) | `pytest tests/test_async_service.py -v` |

---

## 💻 Instruções de Configuração do Ambiente

Para configurar o ambiente Python e executar os testes:

```bash
# 1. Navegar até o diretório do seminário
cd Seminario

# 2. Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# 4. Executar os testes
pytest

# 5. Executar script de demonstração guiada
./demo_script.sh
```

---

## 📋 Regras de Manutenção de Código e Testes

Ao atualizar ou estender este projeto, os agentes e desenvolvedores devem seguir as regras:

1. **Asserções Simples:** Utilize sempre a declaração `assert` nativa do Python. O pytest faz reescrita de AST (*AST rewriting*) para fornecer mensagens de erro detalhadas. Evite classes legadas do estilo `unittest.TestCase`.
2. **Injeção de Dependência via Fixtures:** Todas as instâncias compartilhadas ou estados devem ser providos por fixtures no `conftest.py` ou módulos de teste locais.
3. **Parametrização:** Sempre que houver múltiplos casos de borda/equivalência para uma mesma função pura, utilize `@pytest.mark.parametrize`.
4. **Isolamento e Mocks:** Chamadas externas simuladas (gateways de pagamento, email, etc.) devem ser mockadas utilizando a fixture `mocker` do plugin `pytest-mock`.
5. **Marcação de Testes:** Testes com comportamento específico (ex: lentos, assíncronos) devem ser decorados com `@pytest.mark.<nome>` e registrados no `pytest.ini`.
