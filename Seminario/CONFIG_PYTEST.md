# ⚙️ Guia Completo de Configuração: `pytest.ini`

O arquivo [`pytest.ini`](file:///home/mateuszaparoli/ufmg/8_semestre/Teste%20de%20Software/Seminario/pytest.ini) é o **arquivo de configuração central do Pytest**. Ele define regras de descoberta de testes, opções padrão de execução e registra marcadores customizados, garantindo consistência em qualquer máquina de desenvolvimento ou esteira de CI/CD.

---

## 📄 Conteúdo do Arquivo

```ini
[pytest]
minversion = 8.0
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -ra
    --strict-markers
    --strict-config

markers =
    slow: Marca testes lentos (ex: simulação de IO, integração pesada) para filtragem e paralelização
    unit: Marca testes unitários rápidos e isolados
    integration: Marca testes de integração entre múltiplos componentes
    asyncio: Marca testes assíncronos (pytest-asyncio)
```

---

## 🔍 Explicação Linha a Linha

### 1. Seção Principal e Versão Mínima

#### `[pytest]`
- **O que significa:** É o cabeçalho de seção no formato padrão INI.
- **Papel no Pytest:** Informa ao leitor de configurações que todas as diretivas subsequentes pertencem ao Pytest (e não a outras ferramentas que possam compartilhar arquivos de configuração, como `flake8` ou `coverage`).

#### `minversion = 8.0`
- **O que significa:** Define a versão mínima do Pytest exigida para rodar o projeto.
- **Papel no Pytest:** Se algum desenvolvedor ou servidor de CI tentar rodar os testes usando uma versão legada (ex: Pytest 7.x), o Pytest abortará a execução imediatamente com um erro claro. Isso evita comportamentos inesperados causados por incompatibilidade de recursos modernos.

---

### 2. Regras de Descoberta Automática de Testes (*Test Discovery*)

Estas diretivas padronizam como o Pytest localiza os testes sem necessidade de passar caminhos manuais:

#### `testpaths = tests`
- **O que significa:** Diretório(s) padrão onde o Pytest deve procurar os testes.
- **Papel no Pytest:** Ao digitar apenas `pytest` no terminal, o Pytest vai direto na pasta `tests/`. Ele não perde tempo varrendo pastas desnecessárias como `src/`, `.venv/` ou `reports/`, tornando a inicialização muito mais rápida.

#### `python_files = test_*.py`
- **O que significa:** Padrão glob de nomes dos arquivos que contêm testes.
- **Papel no Pytest:** Apenas arquivos Python cujo nome comece com `test_` (ex: `test_validators.py`, `test_checkout.py`) serão importados como suítes de teste. Arquivos auxiliares como `conftest.py` ou módulos dentro de `src/` não são tratados como testes.

#### `python_classes = Test*`
- **O que significa:** Padrão de nomes para classes de teste.
- **Papel no Pytest:** Ao inspecionar um arquivo de teste, o Pytest só coletará métodos de teste dentro de classes que começam com o prefixo `Test` (ex: `TestValidadorCPF`, `TestProcessadorCheckoutComMocks`). Classes utilitárias ou modelos de dados sem esse prefixo são ignorados.

#### `python_functions = test_*`
- **O que significa:** Padrão de nomes para as funções ou métodos de teste.
- **Papel no Pytest:** O Pytest só executará como caso de teste as funções que comecem com `test_` (ex: `test_validacao_cpf()`). Se você criar uma função auxiliar dentro do arquivo de teste (ex: `criar_massa_de_dados()`), ela não será executada como teste por não possuir esse prefixo.

---

### 3. Opções Automáticas de Linha de Comando (`addopts`)

#### `addopts =`
- **O que significa:** *"Additional Options"* (Opções Adicionais).
- **Papel no Pytest:** Todas as flags listadas nesta seção são injetadas **automaticamente** em qualquer execução do comando `pytest`, exatamente como se você as digitasse no terminal toda vez.

#### `    -ra`
- **O que significa:** `-r` ativa o resumo detalhado no final da execução (*short test summary info*). A letra `a` significa *"all except passed"* (todos exceto os que passaram com sucesso).
- **Papel no Pytest:** No final da execução, se houver falhas, erros, testes pulados (*skipped*) ou falhas esperadas (*xfail*), o Pytest exibe uma lista compacta com o motivo e a linha exata de cada um, sem que você precise rolar centenas de linhas de log.

#### `    --strict-markers`
- **O que significa:** Ativa o **modo rigoroso de marcadores**.
- **Papel no Pytest:** Impede o uso de marcadores não registrados. Por exemplo, se alguém digitar por engano `@pytest.mark.slwo` (com erro de digitação em vez de `slow`), o Pytest **trava a execução com erro** em vez de apenas emitir um aviso ignorável. Isso previne que testes deixem de rodar silenciosamente.

#### `    --strict-config`
- **O que significa:** Ativa o **modo rigoroso de configuração**.
- **Papel no Pytest:** Se houver qualquer erro de digitação dentro do próprio arquivo `pytest.ini` (ex: `testpath` sem o `s`), o Pytest acusa erro imediatamente em vez de ignorar silenciosamente a linha incorreta.

---

### 4. Registro e Governança de Marcadores (`markers`)

#### `markers =`
- **O que significa:** Seção onde são declarados todos os marcadores (`@pytest.mark.<nome>`) válidos no projeto, acompanhados de sua descrição.
- **Papel no Pytest:** Permite a documentação formal dos marcadores (visíveis via `pytest --markers`) e validação conjunta com a flag `--strict-markers`.

#### `    slow: Marca testes lentos (ex: simulação de IO, integração pesada) para filtragem e paralelização`
- Registra o marcador `@pytest.mark.slow`. Usado para isolar testes lentos e permitir filtros como `pytest -m "not slow"` (para rodar rápido no dia a dia) ou `pytest -m slow -n auto` (para rodar paralelo com `pytest-xdist`).

#### `    unit: Marca testes unitários rápidos e isolados`
- Registra o marcador `@pytest.mark.unit` para categorizar testes unitários puros.

#### `    integration: Marca testes de integração entre múltiplos componentes`
- Registra o marcador `@pytest.mark.integration` para testes que envolvem integração entre módulos do sistema.

#### `    asyncio: Marca testes assíncronos (pytest-asyncio)`
- Registra o marcador `@pytest.mark.asyncio`, exigido pelo plugin `pytest-asyncio` para identificar e gerenciar a execução de funções assíncronas (`async def` com `await`).

---

## 💡 Comparativo Prático

| Sem `pytest.ini` | Com `pytest.ini` |
| :--- | :--- |
| Necessário digitar comando longo e propenso a esquecimentos:<br>`pytest tests/ -ra --strict-markers --strict-config` | Basta digitar o comando simples no terminal:<br>`pytest` |
| Erros de digitação em marcadores passam silenciosamente como *warnings*. | Erros de digitação em marcadores quebram o teste imediatamente com erro explícito. |
| Varre todas as pastas do projeto (incluindo virtuais). | Foca exclusivamente no diretório `tests/`. |
