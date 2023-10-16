import pytest
from numpy import arange
from numpy import array
from numpy import isinf
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal

from tabatu.tabua_base import TabuaBase
from tabatu.tabua_base import validar_qx
from tests.conftest import qx_completo
from tests.conftest import qx_plato


# noinspection PyMethodMayBeStatic
class TestUnitTestsUtilsTabuaBase:
    def test_validar_qx_retorna_proprio_argumento_quando_todos_os_qxs_sao_validos(self):
        qx = array([0.1, 0.3, 0.5, 0.7, 0.9])
        assert_array_equal(validar_qx(qx), qx)

    def test_validar_qx_retorna_erro_quando_algum_elemento_de_qx_eh_negativo(self):
        qx = array([-0.1, 0.3, 0.5, 0.7, 0.9])
        with pytest.raises(ValueError):
            validar_qx(qx)

    def test_validar_qx_retorna_erro_quando_algum_elemento_de_qx_eh_maior_que_1(self):
        qx = array([0.1, 0.3, 0.5, 1.7, 0.9])
        with pytest.raises(ValueError):
            validar_qx(qx)

    def test_validar_qx_retorna_erro_quando_qx_possui_mais_que_uma_dimensao(self):
        qx = array([[0.1, 0.3, 0.5, 0.7, 0.9]])
        with pytest.raises(ValueError):
            validar_qx(qx)


class TestIntegrationTestsTempoFuturoMax:
    @pytest.mark.parametrize("x", [0, 50, 1000])
    def test_tempo_futuro_max_eh_sempre_infinito_para_tabua_plato(self, x):
        tabua = TabuaBase(qx_plato)
        assert isinf(tabua.tempo_futuro_maximo(x))

    def test_tempo_futuro_max_eh_finito_quando_a_tabua_eh_completa(self):
        qx = array([0.1, 0.2, 0.4, 0.8, 1.0])
        tabua = TabuaBase(qx)
        assert tabua.tempo_futuro_maximo(0) == 5
        assert tabua.tempo_futuro_maximo(3) == 2
        assert tabua.tempo_futuro_maximo(50) == 0


class TestIntegrationTestsPossuiFechamentoPlato:
    def test_possui_fechamento_plato_retorna_true_quando_a_tabua_eh_plato(self):
        tabua = TabuaBase(qx_plato)
        assert tabua.possui_fechamento_plato()

    def test_possui_fechamento_plato_retorna_false_quando_a_tabua_eh_completa(self):
        tabua = TabuaBase(qx_completo)
        assert not tabua.possui_fechamento_plato()


class TestIntegrationTestsTabuaBaseQx:
    def test_qx_eh_igual_a_1_quando_x_mais_t_for_maior_ou_igual_ao_tempo_futuro_max_e_a_tabua_eh_completa(self):
        """A probabilidade de morte no tempo futuro máximo é sempre 1."""
        tabua = TabuaBase(qx_completo)
        assert (tabua.qx(0, [10, 50, 100]) == 1).all()

    def test_qx_eh_igual_ao_ultimo_qx_quando_x_mais_t_for_maior_ou_igual_ao_tempo_futuro_max_e_a_tabua_eh_plato(self):
        """A probabilidade de morte no tempo futuro máximo é sempre 0."""
        tabua = TabuaBase(qx_plato)
        assert (tabua.qx(0, [10, 50, 100]) == qx_plato[-1]).all()

    def test_qx_retorna_erro_se_t_for_negativo(self):
        tabua = TabuaBase(qx_plato)
        with pytest.raises(ValueError):
            tabua.qx(0, [-1])

    def test_qx_retorna_erro_se_x_for_negativo(self):
        tabua = TabuaBase(qx_plato)
        with pytest.raises(ValueError):
            tabua.qx(-1, [0])


class TestIntegrationTestsTabuaBaseTpx:
    @pytest.mark.parametrize("x", [0, 3, 10])
    @pytest.mark.parametrize("qx", [qx_plato, qx_completo])
    def test_tpx_eh_igual_a_1_quando_t_for_igual_a_0(self, qx, x):
        """A probabilidade de sobrevivência no tempo 0 é sempre 1."""
        tabua = TabuaBase(qx)
        assert tabua.tpx(x, [0]) == array([1])

    def test_tpx_eh_igual_a_0_quando_t_for_maior_ou_igual_ao_tempo_futuro_max_e_a_tabua_completa(self):
        """A probabilidade de sobreviver ao tempo futuro máximo da tábua é zero."""
        tabua = TabuaBase(qx_completo)
        t = arange(3) + tabua.tempo_futuro_maximo(3)
        assert (tabua.tpx(3, t) == 0).all()

    def test_tpx_eh_igual_a_zero_quando_x_maior_ou_igual_ao_tempo_futuro_max_t_maior_que_zero_e_tabua_completa(self):
        """Quando a idade já é acima do tempo futuro máximo da tábua, a probabilidade de sobreviver por pelo menos
        mais 1 tempo é zero."""
        tabua = TabuaBase(qx_completo)
        x = tabua.tempo_futuro_maximo(0) + 1
        t = [1, 2, 3]
        assert (tabua.tpx(x, t) == 0).all()

    @pytest.mark.parametrize("qx", [qx_plato, qx_completo])
    def test_tpx_termina_com_zero(self, qx):
        """A probabilidade de sobreviver tende a zero quando t tende a infinito."""
        tabua = TabuaBase(qx)
        x = 2
        t = min(tabua.tempo_futuro_maximo(x), 100)
        assert tabua.tpx(x, [t]) == pytest.approx(0)

    def test_tpx_retorna_erro_se_t_for_negativo(self):
        tabua = TabuaBase(qx_plato)
        with pytest.raises(ValueError):
            tabua.tpx(0, [-1])

    def test_tpx_retorna_erro_se_x_for_negativo(self):
        tabua = TabuaBase(qx_plato)
        with pytest.raises(ValueError):
            tabua.tpx(-1, [0])


class TestIntegrationTestsTabuaBaseTqx:
    @pytest.mark.parametrize("x", [0, 3, 10])
    @pytest.mark.parametrize("qx", [qx_plato, qx_completo])
    def test_t_qx_soma_1_quando_t_sao_todos_os_tempos_futuros(self, x, qx):
        """A probabilidade de falha em algum tempo futuro é 1."""
        tabua = TabuaBase(qx)
        limite = min(tabua.tempo_futuro_maximo(x), 100)
        t = arange(limite + 1)
        assert sum(tabua.t_qx(x, t)) == pytest.approx(1)

    def test_t_qx_eh_igual_a_1_quando_t_eh_zero_e_x_eh_superior_ao_tempo_futuro_maximo_e_tabua_completa(self):
        """Supondo que o indivíduo excedeu o tempo limite da tábua, a probabilidade de falhar antes do próximo
        aniversário é igual a 1."""
        qx = array([0.1, 0.2, 0.4, 0.8, 1.0])
        tabua = TabuaBase(qx)
        x = tabua.tempo_futuro_maximo(0)
        t = [0]
        assert_array_equal(tabua.t_qx(x - 2, t), array([0.8]))
        assert_array_equal(tabua.t_qx(x, t), array([1.0]))
        assert_array_equal(tabua.t_qx(x + 2, t), array([1.0]))

    def test_t_qx_eh_igual_a_zero_quando_x_eh_superior_ao_tempo_futuro_max_e_t_eh_maior_que_zero_e_tabua_completa(self):
        """Supondo que o indivíduo excedeu o tempo limite da tábua, a probabilidade de falhar antes do próximo
        aniversário é 1, logo, a probabilidade de sobreviver ao próximo aniversário e falhar em algum tempo futuro é
        zero."""
        tabua = TabuaBase(qx_completo)
        x = tabua.tempo_futuro_maximo(0) + 1
        t = [1, 2, 3]
        assert (tabua.t_qx(x, t) == 0).all()

    def test_t_qx_retorna_erro_se_t_for_negativo(self):
        tabua = TabuaBase(qx_plato)
        with pytest.raises(ValueError):
            tabua.t_qx(0, [-1])

    def test_t_qx_retorna_erro_se_x_for_negativo(self):
        tabua = TabuaBase(qx_plato)
        with pytest.raises(ValueError):
            tabua.t_qx(-1, [0])
