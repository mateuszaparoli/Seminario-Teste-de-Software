# 🔍 Guia Prático: Inspeção de Plugins, Controle de Execução e Debug no Pytest

Este guia apresenta o passo a passo técnico e os comandos para demonstrar no seminário como inspecionar plugins ativos, como alternar entre modos de visualização (com e sem plugins como `pytest-sugar`), e como depurar testes com falhas utilizando as ferramentas nativas do Pytest.

---

## 🧩 1. Como Inspecionar Plugins Ativos no Pytest

O ecossistema do Pytest utiliza o mecanismo de **Entry Points** do Python (`pytest11`) para carregar automaticamente qualquer plugin instalado no ambiente virtual (`.venv`).

### A. Inspeção Rápida no Cabeçalho de Execução
Ao executar qualquer comando `pytest` (ou `pytest -v`), o Pytest imprime logo nas primeiras linhas do cabeçalho da sessão todos os plugins de terceiros carregados e suas versões:

```bash
pytest
```

**Exemplo de Saída no Terminal:**
```text
Test session starts (platform: linux, Python 3.12.3, pytest 9.1.1, pytest-sugar 1.1.1)
rootdir: /home/mateuszaparoli/ufmg/8_semestre/Teste de Software/Seminario
configfile: pytest.ini
testpaths: tests
plugins: cov-7.1.0, metadata-3.1.1, xdist-3.8.0, sugar-1.1.1, html-4.2.0, asyncio-1.4.0, mock-3.15.1
```

> **Explicação Teórica:** A linha `plugins:` confirma exatamente quais extensões foram descobertas e ativadas para a sessão de testes atual.

---

### B. Diagnóstico Completo com `--trace-config` (O "Raio-X" do Pytest)
Para visualizar a árvore completa de plugins (internos do núcleo, hooks de configuração e plugins externos):

```bash
pytest --trace-config -k "none"
```

**O que este comando revela:**
1. **Plugins Internos do Pytest:** `mark`, `fixtures`, `debugging`, `runner`, `assertion`, `capture`, `logging`, `reports`, etc.
2. **Plugins Externos Instalados:** Caminhos absolutos dos arquivos de plugins no `.venv` (`pytest_sugar.py`, `pytest_mock`, `pytest_cov`, `xdist`, etc.).
3. **Hooks Locais:** Carregamento do arquivo `tests/conftest.py`.

---

### C. Listagem via Gerenciador de Pacotes (`pip`)
Para verificar os pacotes de plugins instalados no ambiente virtual:

```bash
pip list | grep pytest
```

---

## 🎨 2. Demonstração: Execução COM e SEM o `pytest-sugar`

O plugin `pytest-sugar` altera a forma como o Pytest reporta o progresso no terminal, substituindo a saída tradicional por uma interface gráfica em tempo real.

### A. Execução COM `pytest-sugar` (Padrão)
```bash
pytest
```
* **Características:**
  * Barra de progresso dinâmica (`██████████ 100%`).
  * Ícones visuais de status (`✓` verde para aprovado, `⨯` vermelho para falha).
  * Exibição instantânea de erros (não espera o final da suíte para mostrar a falha).
  * Cronômetro de tempo de execução por teste.

---

### B. Execução SEM `pytest-sugar` (Pytest Clássico / Vanilla)
Para desativar temporariamente um plugin sem precisar desinstalá-lo do `.venv`, utilize a flag **`-p no:<nome_do_plugin>`**:

```bash
pytest -p no:sugar
```

ou com saída detalhada (*verbose*):

```bash
pytest -p no:sugar -v
```

* **Características:**
  * Saída textual clássica com pontos (`.`) para sucesso, `F` para falha e `s` para pulado (*skipped*).
  * Porcentagem de progresso calculada arquivo por arquivo no final de cada linha.

> **Dica para o Seminário:** A flag `-p no:<nome_do_plugin>` funciona com **qualquer plugin** do Pytest:
> * Desativar cobertura: `pytest -p no:cov`
> * Desativar paralelização: `pytest -p no:xdist`
> * Desativar suporte assíncrono: `pytest -p no:asyncio`

---

## 🐛 3. Demonstração: Testes com Falha e Estratégias de Debug

O Pytest oferece um conjunto poderoso de recursos para investigar por que um teste quebrou.

### A. Introspecção de Asserções (*AST Rewriting*)
Ao contrário do `unittest` clássico (que exige métodos verbosos como `self.assertEqual(a, b)` para fornecer mensagens claras), o Pytest reescreve a Árvore Sintática Abstrata (AST) do Python em tempo de carregamento.

Quando um `assert` nativo falha, o Pytest decompõe os valores intermediários:

```python
# Exemplo de teste com falha:
def test_exemplo_falha(carrinho_com_produtos):
    assert carrinho_com_produtos.subtotal == Decimal("100.00")
```

**Saída gerada pelo Pytest:**
```text
________________________ test_exemplo_falha ________________________

carrinho_com_produtos = Carrinho(itens=[...], cupom=None)

    def test_exemplo_falha(carrinho_com_produtos):
>       assert carrinho_com_produtos.subtotal == Decimal("100.00")
E       assert Decimal('150.00') == Decimal('100.00')
E        +  where Decimal('150.00') = Carrinho(...).subtotal
```

---

### B. Exibindo Variáveis Locais com `-l` (`--showlocals`)
Ao usar `-l` ou `--showlocals`, o Pytest imprime uma tabela com os valores de **todas as variáveis locais** da função no momento exato em que a falha ocorreu:

```bash
pytest -l -p no:sugar
```

Isso evita a necessidade de adicionar múltiplos `print()` no código para inspecionar o estado das variáveis.

---

### C. Debug Interativo com `--pdb` (Post-Mortem Debugging)
A flag `--pdb` instrui o Pytest a interromper o processo e abrir o debugger interativo do Python (`pdb`) na linha exata onde ocorreu a exceção ou falha de asserção:

```bash
pytest --pdb
```

**Comandos úteis dentro do prompt `(Pdb)`:**
* `p <variavel>`: Imprime o valor da variável (ex: `p cart.itens`).
* `locals()`: Exibe todas as variáveis locais disponíveis no escopo.
* `pp <expressao>`: *Pretty-print* para estruturas de dados complexas.
* `n` (*next*): Executa a próxima linha.
* `c` (*continue*): Continua a execução até a próxima falha.
* `q` (*quit*): Encerra o debugger e sai da execução de testes.

---

### D. Uso de `breakpoint()` e a Flag `-s` (`--capture=no`)
Por padrão, o Pytest captura e oculta saídas padrão (`stdout`/`stderr`). Para utilizar chamadas manuais à função nativa `breakpoint()` ou visualizar comandos `print()`:

```bash
pytest -s
```

---

### E. Otimização do Fluxo de Correção: `--lf` e `--ff`

Depois de identificar e corrigir um bug, não é necessário reexecutar toda a suíte de testes:

1. **`--lf` (`--last-failed`):** Executa **apenas** os testes que falharam na última rodada:
   ```bash
   pytest --lf
   ```

2. **`--ff` (`--failed-first`):** Executa primeiro os testes que falharam e, caso passem, roda o restante da suíte:
   ```bash
   pytest --ff
   ```

*(Essas informações são salvas automaticamente pelo Pytest no diretório local `.pytest_cache/`)*.

---

## 📊 4. Tabela Resumo de Comandos para Apresentação

| Cenário de Demonstração | Comando | Benefício / Destaque |
| :--- | :--- | :--- |
| **Inspecionar plugins ativos** | `pytest` | Visualização rápida na linha `plugins:` do cabeçalho |
| **Raio-X de plugins e hooks** | `pytest --trace-config` | Exibe plugins internos, externos e `conftest.py` |
| **Execução moderna com Sugar** | `pytest` | Barra de progresso, cores e tempos em tempo real |
| **Execução clássica (Sem Sugar)** | `pytest -p no:sugar` | Demonstra como desligar plugins via `-p no:<plugin>` |
| **Modo verboso clássico** | `pytest -p no:sugar -v` | Detalhamento teste a teste no formato tradicional |
| **Mostrar variáveis locais no erro** | `pytest -l` | Inspeciona variáveis locais sem alterar o código |
| **Debug interativo na falha** | `pytest --pdb` | Abre o Python Debugger no ponto exato da exceção |
| **Reexecutar apenas as falhas** | `pytest --lf` | Acelera o ciclo de feedback durante correções |
