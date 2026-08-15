# Guia Completo de Estudo e Preparação: Pytest e seus Plugins

Este documento foi elaborado para fornecer todo o embasamento teórico, prático e metodológico necessário para apresentar com excelência o seminário de **Teste de Software** no DCC/UFMG sobre o tema **"Pytest e seus Plugins"**.

---

## 📑 Sumário

1. [O que é o Pytest e por que ele revolucionou o ecossistema Python?](#1-o-que-é-o-pytest-e-por-que-ele-revolucionou-o-ecossistema-python)
2. [Arquitetura e Recursos Fundamentais](#2-arquitetura-e-recursos-fundamentais)
   - [2.1 Asserções Nativas e AST Rewriting](#21-asserções-nativas-e-ast-rewriting)
   - [2.2 O Sistema de Fixtures e Injeção de Dependências](#22-o-sistema-de-fixtures-e-injeção-de-dependências)
   - [2.3 O Arquivo `conftest.py` e Descoberta Automática](#23-o-arquivo-conftestpy-e-descoberta-automática)
   - [2.4 Parametrização de Testes (`@pytest.mark.parametrize`)](#24-parametrização-de-testes-pytestmarkparametrize)
   - [2.5 Sistema de Marcadores (*Markers*)](#25-sistema-de-marcadores-markers)
   - [2.6 Teste de Exceções (`pytest.raises`)](#26-teste-de-exceções-pytestraises)
3. [O Ecossistema de Plugins e o Framework Pluggy](#3-o-ecossistema-de-plugins-e-o-framework-pluggy)
4. [Análise Detalhada dos Plugins Utilizados na Demonstração](#4-análise-detalhada-dos-plugins-utilizados-na-demonstração)
   - [`pytest-sugar`](#41-pytest-sugar)
   - [`pytest-cov`](#42-pytest-cov)
   - [`pytest-mock`](#43-pytest-mock)
   - [`pytest-xdist`](#44-pytest-xdist)
   - [`pytest-html`](#45-pytest-html)
   - [`pytest-asyncio`](#46-pytest-asyncio)
5. [Roteiro de Fala Passo a Passo para a Apresentação (Com Tempos)](#5-roteiro-de-fala-passo-a-passo-para-a-apresentação-com-tempos)
6. [Guia de Execução da Demonstração Prática (Live Demo)](#6-guia-de-execução-da-demonstração-prática-live-demo)
7. [Perguntas Difíceis que o Professor ou Colegas Podem Fazer (e Como Responder)](#7-perguntas-difíceis-que-o-professor-ou-colegas-podem-fazer-e-como-responder)

---

## 1. O que é o Pytest e por que ele revolucionou o ecossistema Python?

Historicamente, o suporte nativo a testes em Python foi baseado no módulo `unittest` da biblioteca padrão, criado inspirado diretamente no JUnit (Java) e na arquitetura xUnit de Kent Beck. 

Embora funcional, o `unittest` impõe forte acoplamento com o paradigma de Orientação a Objetos:
- Obriga toda suíte a herdar de `unittest.TestCase`.
- Obriga o desenvolvedor a memorizar dezenas de métodos de asserção como `self.assertEqual`, `self.assertTrue`, `self.assertAlmostEqual`, `self.assertRaises`.
- Possui um modelo rígido de ciclo de vida com `setUp()` e `tearDown()`, onde o reaproveitamento de dados entre arquivos de teste gera heranças profundas e frágeis.

O **Pytest** surgiu com uma filosofia radicalmente diferente:
1. **Pythonicidade e Simplicidade:** Testes podem ser simples funções soltas (`def test_algo():`), sem classes obrigatórias nem herança forçada.
2. **Uso da palavra-chave `assert` nativa:** Você escreve `assert a == b`, e o framework cuida de explicar exatamente onde e como falhou.
3. **Injeção de Dependências com Fixtures:** Substitui o antigo `setUp/tearDown` por funções reutilizáveis, modulares e composíveis.
4. **Arquitetura Aberta de Plugins:** Quase todo o comportamento interno do Pytest pode ser interceptado e estendido através de ganchos (*hooks*).

Hoje, o Pytest é o padrão *de facto* adotado por empresas como Meta, Google, Netflix, Dropbox, e projetos open-source como Django, FastAPI, Pandas e NumPy.

---

## 2. Arquitetura e Recursos Fundamentais

### 2.1 Asserções Nativas e AST Rewriting

Uma das maiores dúvidas em bancas de seminário é: *"Se o Python possui a declaração `assert` que apenas lança `AssertionError` sem detalhes, como o Pytest consegue mostrar comparações detalhadas de listas, dicionários e objetos?"*

**Resposta Técnica:**
O Pytest utiliza **AST Rewriting (Reescrita da Árvore Sintática Abstrata)**. Quando o Pytest descobre e importa um arquivo de teste (`test_*.py`), antes de compilá-lo para bytecode Python, ele intercepta o nó de sintaxe `assert` na AST. Ele reescreve essa instrução em tempo de execução para inspecionar cada subexpressão (lado esquerdo, operador, lado direito). Se a condição falhar, ele coleta os valores intermediários e constrói uma mensagem de erro extremamente rica com *diff* visual.

### 2.2 O Sistema de Fixtures e Injeção de Dependências

Fixtures no Pytest são funções decoradas com `@pytest.fixture` que preparam um estado ou fornecem dados para os testes.

**Vantagens sobre o `setUp` clássico:**
- **Injeção Explícita:** Se um teste precisa do carrinho de compras, basta declarar `def test_total(carrinho_com_produtos):`. O Pytest analisa a assinatura da função e injeta o retorno da fixture correspondente.
- **Composição em Camadas:** Uma fixture pode receber outra fixture como argumento. Por exemplo, `carrinho_com_produtos` recebe `cliente_valido` e `itens_padrao`.
- **Escopos (*Scopes*):** Você pode controlar quando a fixture é instanciada e destruída:
  - `scope="function"` (padrão): Executada a cada função de teste (isolamento total).
  - `scope="class"`: Executada uma vez por classe de teste.
  - `scope="module"`: Executada uma vez por arquivo `.py` de teste.
  - `scope="package"`: Executada uma vez por pacote de diretórios.
  - `scope="session"`: Executada uma única vez durante toda a execução da suíte (ideal para conexões com Docker, migrações de banco, etc.).
- **Teardown garantido com `yield`:** Código antes do `yield` roda antes do teste (Setup). Código após o `yield` roda após o término do teste (Teardown), mesmo se o teste falhar com exceção!

### 2.3 O Arquivo `conftest.py` e Descoberta Automática

O arquivo `conftest.py` é uma convenção especial do Pytest. Ele atua como um repositório local ou global de fixtures e configurações.
- **Não requer `import`:** Qualquer fixture definida em um `conftest.py` fica imediatamente disponível para todos os arquivos de teste daquele diretório e subdiretórios.
- **Hierarquia:** Você pode ter um `conftest.py` na raiz de `tests/` com fixtures globais e outro `conftest.py` dentro de uma subpasta de testes de integração com fixtures específicas daquele módulo.

### 2.4 Parametrização de Testes (`@pytest.mark.parametrize`)

Permite aplicar o conceito de **Testes Baseados em Dados (Data-Driven Testing)** e cobrir classes de equivalência e limites com zero duplicação de código.

Exemplo no nosso projeto (`test_validators.py`):
```python
@pytest.mark.parametrize(
    "cpf, esperado",
    [
        ("111.444.777-35", True),
        ("111.111.111-11", False),
        ("123.456.789-00", False),
    ],
    ids=["cpf_valido", "digitos_iguais", "digito_verificador_invalido"]
)
def test_validacao_cpf(cpf, esperado):
    assert validar_cpf(cpf) == esperado
```
O Pytest gera 3 casos de teste independentes no relatório, facilitando identificar exatamente qual combinação de entrada falhou.

### 2.5 Sistema de Marcadores (*Markers*)

Marcadores permitem categorizar testes para execução seletiva.
- Marcadores nativos: `@pytest.mark.skip(reason="...")`, `@pytest.mark.xfail(reason="Bug conhecido")`.
- Marcadores customizados definidos no `pytest.ini`: `@pytest.mark.slow`, `@pytest.mark.unit`, `@pytest.mark.integration`.
- Execução filtrada: `pytest -m "not slow"` ou `pytest -m "integration and not slow"`.

### 2.6 Teste de Exceções (`pytest.raises`)

Testar caminhos de erro é tão crucial quanto o caminho feliz. O Pytest fornece o context manager `pytest.raises`:

```python
with pytest.raises(ValueError, match="Preço unitário não pode ser negativo"):
    Item(nome="Invalido", preco_unitario=-10.0)
```
O parâmetro `match` aceita expressões regulares para validar a mensagem de erro exata.

---

## 3. O Ecossistema de Plugins e o Framework Pluggy

O grande diferencial do Pytest em relação a outros frameworks é que o próprio Pytest foi desenvolvido como um conjunto de plugins construídos sobre o **Pluggy**.

### Como funciona o Pluggy?
1. **Hook Specifications (Especificações de Ganchos):** O Pytest declara ganchos para cada etapa do ciclo de vida:
   - Coleta de testes: `pytest_collect_file`, `pytest_collection_modifyitems`
   - Execução de testes: `pytest_runtest_protocol`, `pytest_runtest_setup`, `pytest_runtest_call`
   - Relatórios: `pytest_report_teststatus`, `pytest_terminal_summary`
2. **Hook Implementations (Implementações):** Qualquer pacote Python instalado no ambiente que declare pontos de entrada (*entrypoints*) no `setup.py`/`pyproject.toml` com a chave `pytest11` é descoberto e registrado automaticamente pelo Pytest.

---

## 4. Análise Detalhada dos Plugins Utilizados na Demonstração

### 4.1 `pytest-sugar`
- **Problema:** A saída padrão do pytest exibe pontos simples (`....F....`) que não oferecem senso claro de progresso em suítes com centenas de testes.
- **Solução:** Adiciona cores vibrantes, barra de progresso gráfica no terminal e exibe falhas instantaneamente à medida que ocorrem.
- **Como demonstrar:** Executar `pytest` e apontar a barra de progresso e as porcentagens em tempo real.

### 4.2 `pytest-cov`
- **Problema:** Saber se os testes estão cobrindo todas as linhas e ramificações críticas do código.
- **Solução:** Integra o Pytest ao `coverage.py`, permitindo gerar relatórios rápidos no terminal com indicação das linhas faltantes e exportar relatórios HTML interativos com visualização linha a linha.
- **Comando:** `pytest --cov=src --cov-report=term-missing --cov-report=html`

### 4.3 `pytest-mock`
- **Problema:** O uso tradicional do `unittest.mock.patch` com decoradores (`@patch(...)`) inverte a ordem dos parâmetros na função, polui a assinatura do teste e pode causar vazamento de estado se o mock não for desfeito em caso de erro.
- **Solução:** Disponibiliza a fixture `mocker`, que oferece métodos como `mocker.patch`, `mocker.patch.object`, `mocker.spy` e `mocker.stub`, garantindo limpeza e desmontagem automática (*teardown*) após cada teste.
- **Demonstração no projeto:** Usado em `test_checkout.py` para simular o gateway de pagamento (aprovação, cartão recusado e timeout de rede) e espionar o serviço de envio de email.

### 4.4 `pytest-xdist`
- **Problema:** Em projetos corporativos, suítes de testes grandes podem demorar minutos ou horas se executadas sequencialmente em um único núcleo de CPU.
- **Solução:** Distribui os testes entre múltiplos processos de CPU ou até mesmo máquinas remotas via SSH.
- **Comando:** `pytest -n auto` (detecta a quantidade de núcleos de CPU disponíveis).
- **Demonstração no projeto:** Em `test_performance_slow.py`, 6 testes com delay passam de **~2.4 segundos** sequenciais para **~0.45 segundos** em paralelo!

### 4.5 `pytest-html`
- **Problema:** Em pipelines de CI/CD ou auditorias de qualidade de software, desenvolvedores e gerentes precisam de relatórios visuais compartilháveis e fáceis de navegar.
- **Solução:** Gera um arquivo HTML autocontido com metadados do ambiente, status dos testes, duração e stack trace detalhado de falhas.
- **Comando:** `pytest --html=reports/report.html --self-contained-html`

### 4.6 `pytest-asyncio`
- **Problema:** O Python assíncrono moderno (`async def`, `await`, corrotinas) não pode ser executado diretamente por runners síncronos padrão.
- **Solução:** Permite marcar testes assíncronos com `@pytest.mark.asyncio`, gerenciando o event loop automaticamente.
- **Demonstração no projeto:** Teste do método `enviar_notificacao_push_async` em `test_async_service.py`.

---

## 5. Roteiro de Fala Passo a Passo para a Apresentação (Com Tempos)

Sugestão de divisão para uma apresentação de **15 a 20 minutos**:

### [00:00 - 03:00] Bloco 1: Introdução e Motivação
- Cumprimentar o professor e a turma.
- Introduzir o tema: *"Hoje vamos falar sobre o Pytest e como seu ecossistema de plugins se tornou a principal referência para testes automatizados em Python."*
- Comparar rapidamente com o modelo clássico do `unittest` (mostrar a tabela de comparação dos slides).
- Destacar a dor de escrever código burocrático e como o Pytest foca em simplicidade e produtividade.

### [03:00 - 07:00] Bloco 2: Os Pilares Nativos do Pytest
- **Asserções:** Explicar o que é o *AST Rewriting* (o Pytest reescreve a árvore sintática para dar mensagens ricas com o simples `assert`).
- **Fixtures:** Explicar como as fixtures resolvem injeção de dependência, escopos e teardown com `yield`.
- **Parametrização:** Explicar o `@pytest.mark.parametrize` para testes orientados a dados.

### [07:00 - 11:00] Bloco 3: O Ecossistema de Plugins
- Explicar a arquitetura baseada no **Pluggy** (sistema de hooks).
- Apresentar os 6 plugins selecionados e a dor que cada um resolve:
  1. `pytest-sugar` (interface visual no terminal)
  2. `pytest-cov` (cobertura de código)
  3. `pytest-mock` (isolamento de dependências com a fixture `mocker`)
  4. `pytest-xdist` (paralelismo em múltiplos núcleos)
  5. `pytest-html` (relatórios para CI/CD)
  6. `pytest-asyncio` (suporte a código assíncrono)

### [11:00 - 16:00] Bloco 4: Demonstração Prática ao Vivo
- Abrir o terminal no diretório `Seminario/`.
- Executar `./demo_script.sh` ou os comandos manuais passo a passo:
  1. Mostrar a execução geral com `pytest` (ver `pytest-sugar` em ação).
  2. Mostrar os testes parametrizados de CPF/Email (`test_validators.py`).
  3. Mostrar o teste de checkout com mock de gateway e spy de notificação (`test_checkout.py`).
  4. Mostrar a comparação de tempo: `pytest tests/test_performance_slow.py` sequencial (~2.4s) vs `pytest tests/test_performance_slow.py -n auto` paralelo (~0.5s).
  5. Mostrar os testes assíncronos (`test_async_service.py`).
  6. Gerar o relatório de cobertura e abrir o arquivo HTML `reports/report.html` no navegador.

### [16:00 - 18:00] Bloco 5: Melhores Práticas e Conclusão
- Recapitular as boas práticas (independência de testes, uso de conftest, markers organizados no `pytest.ini`).
- Abrir para perguntas da banca e dos colegas.

---

## 6. Guia de Execução da Demonstração Prática (Live Demo)

Para garantir que a apresentação ao vivo ocorra com máxima fluidez:

### Preparação Prévia (Antes de começar a apresentação):
```bash
cd "Seminario"
source .venv/bin/activate
# Teste rápido para validar que tudo está verde:
pytest
```

### Opção A: Executar o Script Interativo Automatizado
```bash
./demo_script.sh
```
*(O script pausa entre os passos com explicações coloridas e pede [ENTER] para avançar).*

### Opção B: Comandos Manuais no Terminal durante a Apresentação

1. **Visão Geral e pytest-sugar:**
   ```bash
   pytest
   ```

2. **Parametrização e Asserções:**
   ```bash
   pytest tests/test_validators.py -v
   ```

3. **Mocks e Spies com pytest-mock:**
   ```bash
   pytest tests/test_checkout.py -v
   ```

4. **Paralelismo com pytest-xdist:**
   ```bash
   # Sequencial (~2.4s)
   pytest tests/test_performance_slow.py
   
   # Paralelo (~0.5s)
   pytest tests/test_performance_slow.py -n auto
   ```

5. **Testes Assíncronos:**
   ```bash
   pytest tests/test_async_service.py -v
   ```

6. **Cobertura de Código e Relatório HTML:**
   ```bash
   pytest --cov=src --cov-report=term-missing --html=reports/report.html --self-contained-html
   ```

---

## 7. Perguntas Difíceis que o Professor ou Colegas Podem Fazer (e Como Responder)

### P1: *"Qual a diferença entre usar `unittest.mock.patch` e a fixture `mocker` do `pytest-mock`?"*
**Resposta:**  
O `unittest.mock.patch` é tradicionalmente usado como decorador de função (`@patch(...)`) ou como gerenciador de contexto (`with patch(...)`). Quando usamos decoradores em múltiplos métodos, os parâmetros mockados são injetados na assinatura da função na ordem inversa, tornando o código confuso. Além disso, se uma asserção falhar de forma atípica, o teardown do mock pode vazar para outros testes.  
A fixture `mocker` do `pytest-mock` é injetada diretamente via DI do Pytest, possui sintaxe limpa e garante que 100% dos mocks, spies e stubs sejam desfeitos com segurança ao final daquele teste específico.

---

### P2: *"Como o `pytest-xdist` garante o isolamento entre os processos paralelos?"*
**Resposta:**  
O `pytest-xdist` utiliza a biblioteca `execnet` para instanciar processos Python completamente separados (subprocessos do sistema operacional). Cada processo recebe um subconjunto de testes para executar e comunica o resultado de volta ao processo principal via serialização IPC.  
Por serem processos distintos com espaço de memória isolado, variáveis globais em memória não colidem entre workers. No entanto, é responsabilidade do desenvolvedor garantir que recursos externos compartilhados (como um banco de dados real em disco ou arquivo compartilhado) não sofram condições de corrida (*race conditions*), ou utilizar fixtures com identificadores únicos por worker (`worker_id`).

---

### P3: *"Por que o Pytest não precisa de arquivos `__init__.py` obrigatórios em todas as pastas de teste?"*
**Resposta:**  
O Pytest implementa seu próprio mecanismo de descoberta e importação de módulos. Ele adiciona o diretório raiz do projeto ao `sys.path` dinamicamente durante a inicialização (conforme configurado no `pytest.ini` ou `pyproject.toml`). O uso de `__init__.py` dentro da pasta `tests/` é opcional, sendo recomendado principalmente se você tiver arquivos de teste com o mesmo nome em subpastas diferentes para evitar colisões no namespace de módulos do Python.

---

### P4: *"O que é AST Rewriting e por que isso não torna os testes lentos?"*
**Resposta:**  
A reescrita de AST acontece apenas no momento da importação do arquivo de teste pelo Pytest. O Pytest faz o parsing do código fonte Python, modifica os nós de `Assert` na árvore sintática para injetar chamadas de captura de valores intermediários e compila para bytecode.  
O impacto de desempenho é praticamente imperceptível (na casa dos milissegundos na importação inicial), e em troca ganhamos a legibilidade de escrever asserções em Python puro sem overhead durante a execução repetida dos testes.
