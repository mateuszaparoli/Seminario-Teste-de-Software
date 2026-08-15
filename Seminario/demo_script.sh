#!/usr/bin/env bash
# ==============================================================================
# Script de Demonstração Interativa para Apresentação de Seminário
# Tema: Pytest e seus Plugins: Da Teoria à Prática
# DCC / UFMG - Teste de Software
# ==============================================================================

# Cores para saída no terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Ativar ambiente virtual se existir
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

clear
echo -e "${CYAN}${BOLD}====================================================================${NC}"
echo -e "${GREEN}${BOLD}     SEMINÁRIO: PYTEST E SEUS PLUGINS - ROTEIRO DE DEMONSTRAÇÃO     ${NC}"
echo -e "${CYAN}${BOLD}====================================================================${NC}"
echo -e "Este script executa passo a passo a demonstração ao vivo para a apresentação."
echo ""

pausar() {
    echo ""
    echo -e "${YELLOW}>> Pressione [ENTER] para avançar para o próximo passo...${NC}"
    read -r
    clear
}

# ------------------------------------------------------------------------------
# PASSO 1: Execução Básica com pytest-sugar
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[PASSO 1/6] Execução Básica + Plugin 'pytest-sugar'${NC}"
echo -e "${CYAN}O que vamos demonstrar:${NC}"
echo -e " - Execução nativa do Pytest com visualização aprimorada pelo plugin ${BOLD}pytest-sugar${NC}."
echo -e " - Barra de progresso dinâmica, status visual de cada teste e relatório de tempo."
echo ""
echo -e "${YELLOW}Comando:${NC} pytest"
echo "--------------------------------------------------------------------"
pytest
pausar

# ------------------------------------------------------------------------------
# PASSO 2: Asserções Nativas e Parametrização (@pytest.mark.parametrize)
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[PASSO 2/6] Recursos Nativos: Asserções & Parametrização (@pytest.mark.parametrize)${NC}"
echo -e "${CYAN}O que vamos demonstrar:${NC}"
echo -e " - Testes de validadores (CPF, Email, Cupons)."
echo -e " - 10 casos de teste gerados dinamicamente com nomes descritivos (IDs)."
echo ""
echo -e "${YELLOW}Comando:${NC} pytest tests/test_validators.py -v"
echo "--------------------------------------------------------------------"
pytest tests/test_validators.py -v
pausar

# ------------------------------------------------------------------------------
# PASSO 3: Plugin 'pytest-mock' (Mocking Elegante e Seguro)
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[PASSO 3/6] Plugin 'pytest-mock': Fixture mocker, Spies e Stubs${NC}"
echo -e "${CYAN}O que vamos demonstrar:${NC}"
echo -e " - Mock de gateway de pagamento externo sem decorators verbosos."
echo -e " - Spy no serviço de e-mail (verificando que email só é enviado se pagamento aprovar)."
echo -e " - Simulação de timeout e recusa de cartão."
echo ""
echo -e "${YELLOW}Comando:${NC} pytest tests/test_checkout.py -v"
echo "--------------------------------------------------------------------"
pytest tests/test_checkout.py -v
pausar

# ------------------------------------------------------------------------------
# PASSO 4: Plugin 'pytest-xdist' (Execução Paralela Distribuída)
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[PASSO 4/6] Plugin 'pytest-xdist': Paralelização por Processos/Núcleos de CPU${NC}"
echo -e "${CYAN}O que vamos demonstrar:${NC}"
echo -e " 1. Execução sequencial de 6 testes lentos (~2.4s):"
echo -e "${YELLOW}Comando:${NC} pytest tests/test_performance_slow.py"
echo "--------------------------------------------------------------------"
pytest tests/test_performance_slow.py
echo ""
echo -e "${CYAN} 2. Execução PARALELA distribuída com ${BOLD}pytest-xdist (-n auto)${NC} (~0.5s):"
echo -e "${YELLOW}Comando:${NC} pytest tests/test_performance_slow.py -n auto"
echo "--------------------------------------------------------------------"
pytest tests/test_performance_slow.py -n auto
pausar

# ------------------------------------------------------------------------------
# PASSO 5: Plugin 'pytest-asyncio' (Testes Assíncronos Modernos)
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[PASSO 5/6] Plugin 'pytest-asyncio': Testes Assíncronos com async/await${NC}"
echo -e "${CYAN}O que vamos demonstrar:${NC}"
echo -e " - Teste de corrotina com envio assíncrono de notificações push usando @pytest.mark.asyncio."
echo ""
echo -e "${YELLOW}Comando:${NC} pytest tests/test_async_service.py -v"
echo "--------------------------------------------------------------------"
pytest tests/test_async_service.py -v
pausar

# ------------------------------------------------------------------------------
# PASSO 6: Plugins 'pytest-cov' e 'pytest-html' (Relatórios de Cobertura e HTML)
# ------------------------------------------------------------------------------
echo -e "${BLUE}${BOLD}[PASSO 6/6] Plugins 'pytest-cov' & 'pytest-html': Cobertura e Relatório Visual${NC}"
echo -e "${CYAN}O que vamos demonstrar:${NC}"
echo -e " - Medição de cobertura de código no terminal com linhas faltantes (--cov-report=term-missing)."
echo -e " - Geração de relatório HTML standalone (--html=reports/report.html)."
echo ""
echo -e "${YELLOW}Comando:${NC} pytest --cov=src --cov-report=term-missing --html=reports/report.html --self-contained-html"
echo "--------------------------------------------------------------------"
pytest --cov=src --cov-report=term-missing --html=reports/report.html --self-contained-html
echo ""
echo -e "${GREEN}${BOLD}Relatório HTML gerado em: ${CYAN}Seminario/reports/report.html${NC}"
echo ""
echo -e "${GREEN}${BOLD}====================================================================${NC}"
echo -e "${GREEN}${BOLD}               DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!                  ${NC}"
echo -e "${GREEN}${BOLD}====================================================================${NC}"
