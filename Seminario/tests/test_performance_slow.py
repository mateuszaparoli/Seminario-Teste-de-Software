"""
test_performance_slow.py - Demonstração do Plugin 'pytest-xdist' e Markers (@pytest.mark.slow).

O plugin 'pytest-xdist' permite distribuir a execução dos testes em múltiplos processos/núcleos de CPU:
- Comando sequencial padrão: 'pytest tests/test_performance_slow.py' (demora ~2.4s)
- Comando paralelo distribuído: 'pytest tests/test_performance_slow.py -n auto' (demora ~0.5s!)
- Filtragem por marcador: 'pytest -m "not slow"' (ignora estes testes lentos)
"""
import time
import pytest


@pytest.mark.slow
class TestOperacoesLentasIntegracao:
    """Simula testes pesados de integração ou comunicação de rede."""

    def test_sincronizacao_estoque_armazem_1(self):
        time.sleep(0.4)
        assert True

    def test_sincronizacao_estoque_armazem_2(self):
        time.sleep(0.4)
        assert True

    def test_validacao_antifraude_pesada(self):
        time.sleep(0.4)
        assert True

    def test_emissao_nota_fiscal_sefaz(self):
        time.sleep(0.4)
        assert True

    def test_conciliacao_bancaria_noturna(self):
        time.sleep(0.4)
        assert True

    def test_backup_transacional_s3(self):
        time.sleep(0.4)
        assert True
