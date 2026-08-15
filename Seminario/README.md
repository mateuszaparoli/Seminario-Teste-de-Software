# Seminário: Pytest e seus Plugins

Repositório com o projeto prático, suíte de testes e materiais de apresentação para o seminário da disciplina **Teste de Software (DCC/UFMG)**.

---

## 📚 Materiais Inclusos

1. **`GUIA_ESTUDO_PYTEST.md`:** Guia completo de estudos, conceitos teóricos aprofundados (AST Rewriting, Fixtures, Pluggy), roteiro de fala cronometrado e respostas para perguntas difíceis.
2. **`SLIDES_APRESENTACAO.md`:** Slides estruturados em Markdown (compatível com Marp, Slidev ou exportação para PDF/PPT).
3. **`demo_script.sh`:** Script interativo com cores no terminal para conduzir a demonstração ao vivo com pausas explicativas.
4. **Projeto Prático (`src/` e `tests/`):** Sistema de E-Commerce com checkout, regras de negócio e suíte completa demonstrando:
   - Asserções nativas e `@pytest.mark.parametrize`
   - Fixtures com injeção de dependência e `yield` teardown no `conftest.py`
   - Plugins: `pytest-sugar`, `pytest-cov`, `pytest-mock`, `pytest-xdist`, `pytest-html`, `pytest-asyncio`

---

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
- Python 3.10 ou superior.

### 2. Ativar Ambiente e Instalar Dependências
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Execução dos Testes
```bash
# Executar todos os testes com barra de progresso do pytest-sugar:
pytest

# Executar a demonstração guiada completa:
./demo_script.sh

# Executar testes em paralelo com pytest-xdist:
pytest tests/test_performance_slow.py -n auto

# Executar com relatório de cobertura e relatório HTML:
pytest --cov=src --cov-report=term-missing --html=reports/report.html --self-contained-html
```

---

## 📁 Estrutura de Pastas

```text
.
├── demo_script.sh                 # Script bash interativo para a demo ao vivo
├── GUIA_ESTUDO_PYTEST.md          # Guia teórico, roteiro de fala e perguntas frequentes
├── SLIDES_APRESENTACAO.md         # Slides da apresentação em Markdown
├── pytest.ini                     # Configurações do Pytest e registro de markers
├── requirements.txt               # Dependências do projeto
├── src/                           # Código da aplicação (E-Commerce)
│   ├── ecommerce/
│   │   ├── checkout.py            # Orquestração do checkout
│   │   ├── models.py              # Item, Cliente, Carrinho, Status
│   │   ├── notification_service.py# Notificações síncronas e assíncronas
│   │   └── payment_service.py     # Gateway de pagamento simulado
│   └── utils/
│       └── validators.py          # Validadores de CPF, email e cupom
├── tests/                         # Suíte de testes automatizados
│   ├── conftest.py                # Fixtures globais compartilhadas
│   ├── test_async_service.py      # Demonstração: pytest-asyncio
│   ├── test_checkout.py           # Demonstração: pytest-mock (mocker & spies)
│   ├── test_models.py             # Demonstração: Fixtures e pytest.raises
│   ├── test_performance_slow.py   # Demonstração: pytest-xdist e markers
│   └── test_validators.py         # Demonstração: Asserções e @pytest.mark.parametrize
└── reports/                       # Relatórios gerados (HTML de testes e cobertura)
```
