"""
test_validators.py - Demonstração dos Recursos Nativos do Pytest:
1. Asserções nativas com 'assert' (sem self.assertEqual, self.assertTrue, etc.)
2. Parametrização de Testes com @pytest.mark.parametrize
3. Teste de Exceções com pytest.raises e verificação de regex com match=
"""
import pytest
from src.utils.validators import validar_cpf, validar_email, calcular_desconto_cupom


class TestValidadorCPF:
    """Testes para o algoritmo de validação de CPF."""

    @pytest.mark.parametrize(
        "cpf, esperado",
        [
            ("111.444.777-35", True),   # Formatado e válido
            ("11144477735", True),     # Sem formatação e válido
            ("529.982.247-25", True),   # Outro CPF válido formatado
            ("52998224725", True),     # Outro CPF válido sem formatação
            ("111.111.111-11", False),  # Sequência de dígitos repetidos
            ("000.000.000-00", False),  # Todos zeros
            ("123.456.789-00", False),  # Dígito verificador incorreto
            ("123", False),             # Tamanho insuficiente
            ("abcdefghijk", False),     # Letras
            (None, False),              # Tipo inválido
        ],
        ids=[
            "cpf_valido_com_pontuacao",
            "cpf_valido_sem_pontuacao",
            "segundo_cpf_valido_com_pontos",
            "segundo_cpf_valido_sem_pontos",
            "cpf_com_digitos_iguais",
            "cpf_todos_zeros",
            "cpf_digito_verificador_invalido",
            "cpf_curto",
            "cpf_letras",
            "cpf_nulo",
        ]
    )
    def test_validacao_cpf(self, cpf, esperado):
        """Demonstração de teste parametrizado com 10 cenários distintos."""
        assert validar_cpf(cpf) == esperado


class TestValidadorEmail:
    """Testes para formato de e-mail."""

    @pytest.mark.parametrize(
        "email, esperado",
        [
            ("aluno@dcc.ufmg.br", True),
            ("professor.teste@ufmg.br", True),
            ("usuario+tag@gmail.com", True),
            ("invalido@", False),
            ("@semusuario.com", False),
            ("espacos @dominio.com", False),
            ("", False),
            (None, False),
        ],
        ids=[
            "email_ufmg_valido",
            "email_com_ponto_valido",
            "email_com_plus_tag",
            "email_sem_dominio",
            "email_sem_usuario",
            "email_com_espacos",
            "email_string_vazia",
            "email_nulo",
        ]
    )
    def test_validacao_email(self, email, esperado):
        assert validar_email(email) == esperado


class TestCalculoDescontoCupom:
    """Demonstração de testes parametrizados de regras de cupom e testes de exceções."""

    @pytest.mark.parametrize(
        "cupom, valor_subtotal, desconto_esperado",
        [
            # Cupom DESC10: 10% independente do valor
            ("DESC10", 100.0, 10.0),
            ("desc10", 50.0, 5.0),    # Case insensitive
            ("DESC10", 0.0, 0.0),
            # Cupom DESC20: 20% somente acima de R$ 100
            ("DESC20", 200.0, 40.0),
            ("DESC20", 100.0, 20.0),  # Valor no limite
            ("DESC20", 99.99, 0.0),   # Abaixo do limite de elegibilidade
            # Cupom FRETEGRATIS: R$ 15 fixos para compras >= R$ 50
            ("FRETEGRATIS", 80.0, 15.0),
            ("FRETEGRATIS", 49.99, 0.0),
            # Cupom VIP50: 50% com teto máximo de R$ 100
            ("VIP50", 150.0, 75.0),   # 50% de 150 = 75 (< 100)
            ("VIP50", 300.0, 100.0),  # 50% de 300 = 150 -> limitado a 100.0
            # Sem cupom
            (None, 200.0, 0.0),
            ("", 200.0, 0.0),
        ]
    )
    def test_calculo_descontos_validos(self, cupom, valor_subtotal, desconto_esperado):
        resultado = calcular_desconto_cupom(cupom, valor_subtotal)
        assert resultado == desconto_esperado

    def test_cupom_inexistente_deve_lancar_excecao(self):
        """
        DEMONSTRAÇÃO DE pytest.raises:
        Verifica se a exceção ValueError é lançada com a mensagem correta.
        """
        cupom_invalido = "BLACKFRIDAY99"
        
        with pytest.raises(ValueError, match=f"Cupom inválido ou expirado: '{cupom_invalido}'"):
            calcular_desconto_cupom(cupom_invalido, 100.0)
