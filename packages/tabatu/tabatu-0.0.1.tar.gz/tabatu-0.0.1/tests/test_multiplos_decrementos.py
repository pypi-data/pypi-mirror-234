from unittest.mock import Mock
import pytest
from numpy import array
from numpy.testing import assert_array_equal
from numpy.testing import assert_array_almost_equal

from tabatu import TabuaMDT
from tabatu.multiplos_decrementos import valida_quantidade_tabuas
from tabatu.multiplos_decrementos import captura_argumentos


class TestCapturaArgumentos:
    def test_a_chave_eh_a_posicao_do_argumento_como_string_e_o_valor_eh_a_posicao_quando_argumento_nao_nomeado(
        self,
    ):
        assert captura_argumentos(10, 20) == {"0": 0, "1": 1}

    def test_a_chave_eh_o_nome_e_o_valor_eh_a_posicao_quando_argumento_eh_nomeado(self):
        assert captura_argumentos(a=10, b=20) == {"a": 0, "b": 1}
        assert captura_argumentos(b=10, a=20) == {"b": 0, "a": 1}

    def test_captura_argumentos_funciona_com_argumentos_nomeados_e_nao_nomeados(self):
        assert captura_argumentos(10, b=20) == {"0": 0, "b": 1}



class TestValidaQuantidadeDeTabuas:
    def test_quando_existem_mais_que_3_tabuas_deve_falhar(self):
        with pytest.raises(ValueError):
            valida_quantidade_tabuas(Mock(), Mock(), Mock(), Mock())

    def test_quando_nao_existem_tabuas_deve_falhar(self):
        with pytest.raises(ValueError):
            valida_quantidade_tabuas()

    @pytest.mark.parametrize("args", [(1,), (1, 2), (1, 2, 3)])
    def test_quando_existem_de_uma_a_tres_tabuas_deve_retornar_tupla_com_elas(
        self, args: tuple
    ):
        resultado = valida_quantidade_tabuas(*args)
        assert isinstance(resultado, tuple)
        for i in range(len(args)):
            assert args[i] == resultado[i]


class TestTabuaMDT:
    def test_init_falha_se_causa_principal_eh_invalida(self, mock_tabua1, mock_tabua2):
        with pytest.raises(ValueError):
            TabuaMDT(mock_tabua1, mock_tabua2, causa_principal=3)

        with pytest.raises(ValueError):
            TabuaMDT(mock_tabua1, morte=mock_tabua2, causa_principal="invalidez")

    def test_tpx_eh_o_produto_dos_tpxs_de_cada_tabua(self, tabua_mdt):
        assert tabua_mdt.numero_decrementos == 2

        resultado = tabua_mdt.tpx([1, 2], [2])
        esperado = tabua_mdt.tabuas[0].tpx(1, [2]) * tabua_mdt.tabuas[1].tpx(2, [2])

        assert_array_almost_equal(resultado, esperado)

    @pytest.mark.skip(reason="Não implementado")
    def test_tpx_funciona_com_apenas_uma_idade(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        resultado = tabua.tpx(1, 0)
        mock_tabua1.tabuas[0].tpx.assert_called_once_with(array([1]), 0)
        mock_tabua2.tabuas[0].tpx.assert_called_once_with(array([1]), 0)
        esperado = mock_tabua1.tabuas[0].tpx() * mock_tabua2.tabuas[0].tpx()
        assert_array_equal(resultado, esperado)

    def test_tpx_falha_quando_o_numero_de_tabuas_nao_eh_1_e_nao_eh_compativel_com_o_numero_de_decrementos(
        self, tabua_mdt
    ):
        assert tabua_mdt.numero_decrementos == 2
        with pytest.raises(ValueError):
            tabua_mdt.tpx([1, 1, 1], [0])

    def test_qx_j_retorna_uma_array_com_2_dimensoes(self, tabua_mdt):
        assert tabua_mdt.qx_j([0, 0], [0], [1]).shape == (1, 1)
        assert tabua_mdt.qx_j([0, 0], [0], [0, 1]).shape == (2, 1)

    def test_qx_j_chama_converter_mdt_com_qx_das_tabuas(self, tabua_mdt):
        resultado = tabua_mdt.qx_j([0, 1], [0], [1])
        qx1 = tabua_mdt.tabuas[0].qx(0, [0])
        qx2 = tabua_mdt.tabuas[1].qx(1, [0])
        esperado = qx2 * (1 - 1/2 * qx1)

        assert resultado.item() == esperado.item()

    def test_qx_j_aceita_string_quando_as_tabuas_sao_passadas_por_nome(self, tabua_mdt):
        assert tabua_mdt.causas == {"0": 0, "causa1": 1}
        assert_array_equal(
            tabua_mdt.qx_j([0, 0], [0], [1]), tabua_mdt.qx_j([0, 0], [0], ["causa1"])
        )
        assert_array_equal(
            tabua_mdt.qx_j([0, 0], [0], [0, 1]),
            tabua_mdt.qx_j([0, 0], [0], [0, "causa1"]),
        )

        assert_array_equal(
            tabua_mdt.qx_j([0, 0], [0], ["0", "causa1"]),
            tabua_mdt.qx_j([0, 0], [0], [0, 1]),
        )

    def test_qx_j_falha_quando_o_numero_de_tabuas_nao_eh_1_e_nao_eh_compativel_com_o_numero_de_decrementos(
        self, tabua_mdt
    ):
        assert tabua_mdt.numero_decrementos == 2
        with pytest.raises(ValueError):
            tabua_mdt.qx_j([1, 1, 1], [0], [1])

    def test_qx_chama_qx_j_com_todas_as_causas_e_retorna_array_com_uma_dimensao(
        self, tabua_mdt
    ):
        resultado = tabua_mdt.qx([0, 0], [0, 1, 2])
        qx_j = tabua_mdt.qx_j([0, 0], [0, 1, 2], [0, 1])
        assert_array_equal(resultado, qx_j.sum(axis=0))
        assert resultado.ndim == 1

    def test_tempo_futuro_max_retorna_o_menor_dos_tempos_de_cada_tabua(self, tabua_mdt):
        assert tabua_mdt.tempo_futuro_maximo([4, 4]) == min(
            tabua_mdt.tabuas[0].tempo_futuro_maximo(4),
            tabua_mdt.tabuas[1].tempo_futuro_maximo(4),
        )

    def test_tempo_futuro_maximo_falha_quando_a_quantidadde_de_idades_eh_incompativel(
        self, tabua_mdt
    ):
        assert tabua_mdt.numero_decrementos == 2
        with pytest.raises(ValueError):
            tabua_mdt.tempo_futuro_maximo([5, 5, 5])

    def test_t_qx_considera_apenas_a_causa_principal_quando_ela_eh_fornecida(
        self, tabua_mdt
    ):
        resultado = tabua_mdt.t_qx([1, 2], [0, 1, 2])
        esperado = tabua_mdt.t_qx_j([1, 2], [0, 1, 2], [1]).sum(axis=0)
        assert_array_equal(resultado, esperado)
        assert resultado.ndim == 1
