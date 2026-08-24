# 🚀 Roteiro de Comandos para Apresentação ao Vivo: Pytest e Plugins

Guia prático e direto para consulta rápida durante a apresentação do seminário. Cada etapa possui uma breve explicação de 1 linha seguida do comando exato para copiar e executar no terminal.

---

## ⚙️ 0. Preparação Inicial do Ambiente

Ativar o ambiente virtual com o Pytest e todos os plugins instalados:
```bash
source .venv/bin/activate
```

---

## 📦 1. Rodar o Pytest sem nenhum plugin (Vanilla / Clássico)

Executa os testes desativando todos os plugins para demonstrar a saída textual clássica padrão com pontos (`.`) e porcentagens:
```bash
pytest tests/test_models.py tests/test_validators.py -p no:sugar -p no:cov -p no:xdist -p no:asyncio -p no:mock -p no:html
```

Executa os testes nativos sem plugins no modo detalhado (*verbose*) listando o nome de cada teste individualmente:
```bash
pytest tests/test_models.py tests/test_validators.py -p no:sugar -v
```

Demonstra que a suíte inteira sem plugins falha nos testes que dependem de corrotinas (`async`/`await`) e da fixture `mocker`:
```bash
pytest -p no:sugar -p no:asyncio -p no:mock
```

---

## 🍬 2. Rodar com um plugin específico (ex: apenas o `pytest-sugar`)

Executa o Pytest com o plugin `pytest-sugar` ativo para exibir barra de progresso colorida, ícones de status (`✓`) e tempos em tempo real:
```bash
pytest
```

Executa apenas os testes unitários rápidos isolando a experiência visual do `pytest-sugar`:
```bash
pytest tests/test_models.py tests/test_validators.py
```

---

## 🔌 3. Rodar com os Plugins do Ambiente e Demonstrar cada um

### 3.1 Plugin `pytest-mock` (Dublês de Teste, Spies e Stubs)
Executa os testes de checkout demonstrando mocks de gateway de pagamento e spies de notificação sem decorators verbosos:
```bash
pytest tests/test_checkout.py -v
```

### 3.2 Plugin `pytest-xdist` (Execução Paralela vs Sequencial)
Executa 6 testes lentos de forma sequencial padrão (demora cerca de ~2.4 segundos):
```bash
pytest tests/test_performance_slow.py
```

Executa os mesmos testes distribuídos em paralelo por múltiplos núcleos de CPU com `pytest-xdist` (reduz para ~0.5s):
```bash
pytest tests/test_performance_slow.py -n auto
```

### 3.3 Plugin `pytest-asyncio` (Testes Assíncronos Modernos)
Executa testes de corrotinas assíncronas (`async`/`await`) para envio de notificações push via `@pytest.mark.asyncio`:
```bash
pytest tests/test_async_service.py -v
```

### 3.4 Plugin `pytest-cov` (Relatório de Cobertura de Código)
Executa a suíte medindo a cobertura de código da pasta `src/` e exibindo as linhas não cobertas no terminal:
```bash
pytest --cov=src --cov-report=term-missing
```

### 3.5 Plugin `pytest-html` (Relatório HTML Visual Standalone)
Executa a suíte e gera um relatório HTML independente e interativo na pasta `reports/`:
```bash
pytest --html=reports/report.html --self-contained-html
```

### 3.6 Execução Completa de Todos os Plugins Combinados
Executa toda a suíte integrando visual moderno, cobertura detalhada e geração do relatório HTML em um único comando:
```bash
pytest --cov=src --cov-report=term-missing --html=reports/report.html --self-contained-html
```

Abre o relatório HTML gerado diretamente no navegador web:
```bash
xdg-open reports/report.html
```

---

## 🐛 4. Quebrar Teste, Debugar, Corrigir e Reexecutar com `--lf` / `--ff`

### 4.1 Quebrar um teste propositalmente
Altera o valor esperado do primeiro teste de `tests/test_models.py` para simular uma quebra de regressão:
```bash
sed -i "s/assert item.subtotal == 3600.0/assert item.subtotal == 9999.0/g" tests/test_models.py
```

### 4.2 Executar e observar a falha com AST Rewriting
Executa os testes e demonstra como o Pytest decompõe expressões e exibe claramente a discrepância de valores:
```bash
pytest tests/test_models.py
```

### 4.3 Inspecionar variáveis locais no ponto da falha (`--showlocals`)
Executa exibindo o valor de todas as variáveis locais no exato momento do erro sem precisar colocar `print`:
```bash
pytest tests/test_models.py -l
```

### 4.4 Abrir o depurador interativo no ponto exato da falha (`--pdb`)
Abre o terminal interativo do Python Debugger (`pdb`) no momento em que o `assert` falha:
```bash
pytest tests/test_models.py --pdb
```
> *Comandos úteis dentro do prompt `(Pdb)`:*
> - `p item` *(imprime os dados do objeto)*
> - `locals()` *(lista variáveis locais)*
> - `q` *(digite `q` e pressione [Enter] para sair do debugger)*

### 4.5 Corrigir o teste no código
Restaura o valor correto da asserção no arquivo de teste:
```bash
sed -i "s/assert item.subtotal == 9999.0/assert item.subtotal == 3600.0/g" tests/test_models.py
```

### 4.6 Reexecutar SOMENTE o teste que havia falhado (`--lf` / `--last-failed`)
Usa o cache do Pytest para executar exclusivamente o teste que falhou na última rodada economizando tempo:
```bash
pytest --lf
```

### 4.7 Reexecutar o teste corrigido primeiro e depois o restante (`--ff` / `--failed-first`)
Executa primeiro o teste que havia falhado e, após seu sucesso, roda todo o restante da suíte:
```bash
pytest --ff
```

### 4.8 Rodar toda a suíte e confirmar 100% de aprovação
Executa a suíte completa para comprovar que todos os 56 testes estão verdes e passando com sucesso:
```bash
pytest
```
