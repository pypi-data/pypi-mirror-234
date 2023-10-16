import pytest
from numpy import array
from numpy.testing import assert_array_equal


@pytest.mark.parametrize("x", [array([0]), [0], (0,)])
class TestArgumentosSaoPassadosComoInteirosNosMetodosDeTabua:
    def test_tpx_passa_argumentos_para_tabua_base_quando_x_eh_inteiro_ou_array_like(self, tabua_1dt_1, x):
        assert_array_equal(tabua_1dt_1.tpx([0], [0, 1, 2]), tabua_1dt_1.tpx(x, [0, 1, 2]))

    def test_t_qx_passa_argumentos_para_tabua_base_quando_x_eh_inteiro_ou_array_like(self, tabua_1dt_1, x):
        assert_array_equal(tabua_1dt_1.t_qx([0], [0, 1, 2]), tabua_1dt_1.t_qx(x, [0, 1, 2]))

    def test_qx_passa_argumentos_para_tabua_base_quando_x_eh_array_de_um_elemento(self, tabua_1dt_1, x):
        assert_array_equal(tabua_1dt_1.qx([0], [0, 1, 2]), tabua_1dt_1.qx(x, [0, 1, 2]))

    def test_tempo_futuro_max_passa_argumentos_para_tabua_base_quando_x_eh_array_de_um_elemento(self, tabua_1dt_1, x):
        assert_array_equal(tabua_1dt_1.tempo_futuro_maximo([0]), tabua_1dt_1.tempo_futuro_maximo(x))


@pytest.mark.parametrize("x", [array([0, 0]), [0, 0], (0, 0)])
class TestMetodosFalhamQuandoXPossuiMaisQueUmElemento:
    def test_tpx_falha_quando_x_possui_mais_que_um_elemento(self, tabua_1dt_1, x):
        with pytest.raises(ValueError):
            tabua_1dt_1.tpx(x, [0])

    def test_t_qx_falha_quando_x_possui_mais_que_um_elemento(self, tabua_1dt_1, x):
        with pytest.raises(ValueError):
            tabua_1dt_1.t_qx(x, [0])

    def test_qx_falha_quando_x_possui_mais_que_um_elemento(self, tabua_1dt_1, x):
        with pytest.raises(ValueError):
            tabua_1dt_1.qx(x, [0])

    def test_tempo_futuro_max_falha_quando_x_possui_mais_que_um_elemento(self, tabua_1dt_1, x):
        with pytest.raises(ValueError):
            tabua_1dt_1.tempo_futuro_maximo(x)
