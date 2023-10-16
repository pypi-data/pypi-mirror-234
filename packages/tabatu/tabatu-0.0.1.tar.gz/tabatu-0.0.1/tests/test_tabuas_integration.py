"""Testes que devem passar para todos os tipos de tábuas.
Os testes na tabua base + nas tabaus específicas garantem alguns desses resultados, mas é bom
mantê-los aqui para deixar explicito o comportamento esperado."""
import pytest
from numpy import arange
from numpy import array
from numpy import fromiter
from numpy import isinf
from numpy import mod
from numpy import repeat
from numpy import split
from numpy.testing import assert_array_almost_equal

from tabatu.periodicidade import Periodicidade
from tabatu.periodicidade import converter_periodicidade
from tabatu import StatusVidasConjuntas
from tabatu.alterar_tabua import agravar_qx
from tabatu.alterar_tabua import alterar_periodicidade_qx
from tabatu.multiplas_vidas import TabuaMultiplasVidas
from tabatu.multiplos_decrementos import TabuaMDT
from tabatu.unico_decremento import Tabua
from tests.conftest import qx_completo
from tests.conftest import qx_plato

tabua_base_plato = Tabua(qx_plato)
tabua_mdt_plato_1dt = TabuaMDT(Tabua(qx_plato))
tabua_mdt_plato_2dt = TabuaMDT(Tabua(qx_plato), Tabua(qx_plato))
tabua_mvt_plato_1vida = TabuaMultiplasVidas(Tabua(qx_plato))
tabua_mvt_plato_2vidas = TabuaMultiplasVidas(Tabua(qx_plato), Tabua(qx_plato))
tabua_mvt_plato_2vidas_1completa = TabuaMultiplasVidas(
    Tabua(qx_plato), Tabua(qx_completo), status=StatusVidasConjuntas.LAST
)

tabua_base_completa = Tabua(qx_completo)
tabua_mdt_completa_1dt = TabuaMDT(Tabua(qx_completo))
tabua_mdt_completa_2dt = TabuaMDT(Tabua(qx_completo), Tabua(qx_completo))
tabua_mvt_completa_1vida = TabuaMultiplasVidas(Tabua(qx_completo))
tabua_mvt_completa_2vidas = TabuaMultiplasVidas(Tabua(qx_completo), Tabua(qx_completo))

plato = [tabua_base_plato,
         tabua_mdt_plato_1dt,
         tabua_mdt_plato_2dt,
         tabua_mvt_plato_1vida,
         tabua_mvt_plato_2vidas,
         tabua_mvt_plato_2vidas_1completa, ]

completas = [tabua_base_completa,
             tabua_mdt_completa_1dt,
             tabua_mdt_completa_2dt,
             tabua_mvt_completa_1vida,
             tabua_mvt_completa_2vidas, ]


@pytest.fixture(params=plato)
def tabuas_plato(request):
    return request.param


@pytest.fixture(params=completas)
def tabuas_completas(request):
    return request.param


@pytest.fixture(params=plato + completas)
def todas_tabuas(request):
    return request.param


@pytest.mark.parametrize("x", [0, 50, 1000])
def test_tempo_futuro_max_eh_sempre_infinito_para_tabua_plato(x, tabuas_plato):
    x = repeat(x, tabuas_plato.numero_decrementos * tabuas_plato.numero_vidas)
    assert isinf(tabuas_plato.tempo_futuro_maximo(x))


def test_possui_fechamento_plato_retorna_true_quando_a_tabua_eh_plato(tabuas_plato):
    assert tabuas_plato.possui_fechamento_plato()


def test_possui_fechamento_plato_retorna_false_quando_a_tabua_eh_completa(tabuas_completas):
    assert not tabuas_completas.possui_fechamento_plato()


def test_qx_eh_igual_a_1_quando_x_mais_t_for_maior_ou_igual_ao_tempo_futuro_max_e_a_tabua_eh_completa(tabuas_completas):
    """A probabilidade de morte no tempo futuro máximo é sempre 1."""
    x = repeat(0, tabuas_completas.numero_decrementos * tabuas_completas.numero_vidas)
    assert (tabuas_completas.qx(x, [10, 50, 100]) == 1).all()


def test_qx_eh_igual_ao_ultimo_qx_quando_x_mais_t_for_maior_ou_igual_ao_tempo_futuro_max_e_a_tabua_eh_plato(
    tabuas_plato
):
    """A probabilidade de morte no tempo futuro máximo é sempre 0."""
    x = repeat(0, tabuas_plato.numero_decrementos * tabuas_plato.numero_vidas)
    assert (tabuas_plato.qx(x, [10, 50, 100]) == tabuas_plato.qx(x, [tabuas_plato.tempo_futuro_maximo(x)])).all()


def test_qx_retorna_erro_se_t_for_negativo(todas_tabuas):
    x = repeat(0, todas_tabuas.numero_decrementos * todas_tabuas.numero_vidas)
    with pytest.raises(ValueError):
        todas_tabuas.qx(x, [-1])


def test_qx_retorna_erro_se_x_for_negativo(todas_tabuas):
    x = repeat(-1, todas_tabuas.numero_decrementos * todas_tabuas.numero_vidas)
    with pytest.raises(ValueError):
        todas_tabuas.qx(x, [0])


@pytest.mark.parametrize("x", [0, 3, 10])
def test_tpx_eh_igual_a_1_quando_t_for_igual_a_0(x, todas_tabuas):
    """A probabilidade de sobrevivência no tempo 0 é sempre 1."""
    x = repeat(x, todas_tabuas.numero_decrementos * todas_tabuas.numero_vidas)
    assert todas_tabuas.tpx(x, [0]) == array([1])


def test_tpx_eh_igual_a_0_quando_t_for_maior_ou_igual_ao_tempo_futuro_max_e_a_tabua_completa(tabuas_completas):
    """A probabilidade de sobreviver ao tempo futuro máximo da tábua é zero."""
    x = repeat(3, tabuas_completas.numero_decrementos * tabuas_completas.numero_vidas)
    t = arange(3) + tabuas_completas.tempo_futuro_maximo(x)
    assert (tabuas_completas.tpx(x, t) == 0).all()


def test_tpx_eh_igual_a_zero_quando_x_maior_ou_igual_ao_tempo_futuro_max_t_maior_que_zero_e_tabua_completa(
    tabuas_completas
):
    """Quando a idade já é acima do tempo futuro máximo da tábua, a probabilidade de sobreviver por pelo menos
    mais 1 tempo é zero."""
    x = repeat(0, tabuas_completas.numero_decrementos * tabuas_completas.numero_vidas)
    x = tabuas_completas.tempo_futuro_maximo(x) + 1
    x = repeat(x, tabuas_completas.numero_decrementos * tabuas_completas.numero_vidas)
    t = [1, 2, 3]
    assert (tabuas_completas.tpx(x, t) == 0).all()


def test_tpx_termina_com_zero(todas_tabuas):
    """A probabilidade de sobreviver tende a zero quando t tende a infinito."""
    x = repeat(2, todas_tabuas.numero_decrementos * todas_tabuas.numero_vidas)
    t = min(todas_tabuas.tempo_futuro_maximo(x), 100)
    assert todas_tabuas.tpx(x, [t]) == pytest.approx(0)


def test_tpx_retorna_erro_se_t_for_negativo(todas_tabuas):
    x = repeat(0, todas_tabuas.numero_decrementos * todas_tabuas.numero_vidas)
    with pytest.raises(ValueError):
        todas_tabuas.tpx(x, [-1])


def test_tpx_retorna_erro_se_x_for_negativo(todas_tabuas):
    x = repeat(-1, todas_tabuas.numero_decrementos * todas_tabuas.numero_vidas)
    with pytest.raises(ValueError):
        todas_tabuas.tpx(x, [0])


@pytest.mark.parametrize("x", [0, 3, 10])
def test_t_qx_soma_1_quando_t_sao_todos_os_tempos_futuros(x, todas_tabuas):
    """A probabilidade de falha em algum tempo futuro é 1."""
    x = repeat(x, todas_tabuas.numero_decrementos * todas_tabuas.numero_vidas)
    limite = min(todas_tabuas.tempo_futuro_maximo(x), 100)
    t = arange(limite + 1)
    assert sum(todas_tabuas.t_qx(x, t)) == pytest.approx(1)


def test_t_qx_eh_igual_a_1_quando_t_eh_zero_e_x_eh_superior_ao_tempo_futuro_maximo_e_tabua_completa(tabuas_completas):
    """Supondo que o indivíduo excedeu o tempo limite da tábua, a probabilidade de falhar antes do próximo
    aniversário é igual a 1."""
    x = repeat(0, tabuas_completas.numero_decrementos * tabuas_completas.numero_vidas)
    x = tabuas_completas.tempo_futuro_maximo(x)
    x = repeat(x, tabuas_completas.numero_decrementos * tabuas_completas.numero_vidas)
    t = [0]
    assert (tabuas_completas.t_qx(x - 2, t) < 1).all()
    assert (tabuas_completas.t_qx(x, t) == 1).all()
    assert (tabuas_completas.t_qx(x + 2, t) == 1).all()


def test_t_qx_eh_igual_a_zero_quando_x_eh_superior_ao_tempo_futuro_max_e_t_eh_maior_que_zero_e_tabua_completa(
    tabuas_completas
):
    """Supondo que o indivíduo excedeu o tempo limite da tábua, a probabilidade de falhar antes do próximo
    aniversário é 1, logo, a probabilidade de sobreviver ao próximo aniversário e falhar em algum tempo futuro é
    zero."""
    x = repeat(0, tabuas_completas.numero_decrementos * tabuas_completas.numero_vidas)
    x = tabuas_completas.tempo_futuro_maximo(x) + 1
    x = repeat(x, tabuas_completas.numero_decrementos * tabuas_completas.numero_vidas)
    t = [1, 2, 3]
    assert (tabuas_completas.t_qx(x, t) == 0).all()


def test_t_qx_retorna_erro_se_t_for_negativo(todas_tabuas):
    x = repeat(0, todas_tabuas.numero_decrementos * todas_tabuas.numero_vidas)
    with pytest.raises(ValueError):
        todas_tabuas.t_qx(x, [-1])


def test_t_qx_retorna_erro_se_x_for_negativo(todas_tabuas):
    x = repeat(-1, todas_tabuas.numero_decrementos * todas_tabuas.numero_vidas)
    with pytest.raises(ValueError):
        todas_tabuas.t_qx(x, [0])


@pytest.fixture(
    params=[
        {"menor_periodicidade": Periodicidade.MENSAL, "maior_periodicidade": Periodicidade.TRIMESTRAL},
        {"menor_periodicidade": Periodicidade.MENSAL, "maior_periodicidade": Periodicidade.ANUAL},
        {"menor_periodicidade": Periodicidade.TRIMESTRAL, "maior_periodicidade": Periodicidade.SEMESTRAL},
        {"menor_periodicidade": Periodicidade.BIMESTRAL, "maior_periodicidade": Periodicidade.ANUAL}
    ]
)
def aumentar_periodicidade(request):
    menor_periodicidade = request.param['menor_periodicidade']
    maior_periodicidade = request.param['maior_periodicidade']
    qx_menor_periodicidade = repeat(
        array([0.1, 0.3, 0.5, 1.0]), menor_periodicidade.quantidade_periodos_1_periodicidade(maior_periodicidade)
    )
    qx_maior_periodicidade = alterar_periodicidade_qx(qx_menor_periodicidade, menor_periodicidade, maior_periodicidade)
    tabua_menor_periodicidade = Tabua(qx_menor_periodicidade, menor_periodicidade)
    tabua_maior_periodicidade = Tabua(qx_maior_periodicidade, maior_periodicidade)
    return tabua_menor_periodicidade, tabua_maior_periodicidade


@pytest.fixture(
    params=[
        {"menor_periodicidade": Periodicidade.MENSAL, "maior_periodicidade": Periodicidade.TRIMESTRAL},
        {"menor_periodicidade": Periodicidade.MENSAL, "maior_periodicidade": Periodicidade.ANUAL},
        {"menor_periodicidade": Periodicidade.TRIMESTRAL, "maior_periodicidade": Periodicidade.SEMESTRAL},
        {"menor_periodicidade": Periodicidade.BIMESTRAL, "maior_periodicidade": Periodicidade.ANUAL}
    ]
)
def reduzir_periodicidade(request):
    menor_periodicidade = request.param['menor_periodicidade']
    maior_periodicidade = request.param['maior_periodicidade']
    qx_maior_periodicidade = array([0.1, 0.3, 0.5, 1.0])
    qx_menor_periodicidade = alterar_periodicidade_qx(qx_maior_periodicidade, maior_periodicidade, menor_periodicidade)
    tabua_menor_periodicidade = Tabua(qx_menor_periodicidade, menor_periodicidade)
    tabua_maior_periodicidade = Tabua(qx_maior_periodicidade, maior_periodicidade)
    return tabua_menor_periodicidade, tabua_maior_periodicidade


class TestEfeitoAlteracaoPeriodicidadeNaTabua:
    """
    As tábuas não terão um método para alterá-las. A alteração deve ser feita no momento da criação.
    Isso visa reduzir a chance de uma tábua alterada seja alterada novamente, e a responsabilidade da alteração
    fica no usuário. As tábuas serão sempre válidas desde que o qx seja válido e a periodicidade esteja certa.

    Esses testes estão duplicados para aumento/redução de periodicidade pq não consegui especificar para
    rodar sequencialmeente para as duas fixtures.
    """

    def test_aumentar_periodicidade_nao_altera_o_tempo_futuro_maximo(
        self, aumentar_periodicidade
    ):
        tabua_menor_periodicidade, tabua_maior_periodicidade = aumentar_periodicidade
        maior_periodicidade = tabua_maior_periodicidade.periodicidade
        menor_periodicidade = tabua_menor_periodicidade.periodicidade
        tempo_menor_periodicidade = tabua_menor_periodicidade.tempo_futuro_maximo([0])
        tempo_maior_periodicidade = tabua_maior_periodicidade.tempo_futuro_maximo([0])
        assert tempo_menor_periodicidade - 1 == converter_periodicidade(
            tempo_maior_periodicidade - 1, maior_periodicidade, menor_periodicidade
        ).item()

    def test_reduzir_periodicidade_nao_altera_o_tempo_futuro_max(self, reduzir_periodicidade):
        tabua_menor_periodicidade, tabua_maior_periodicidade = reduzir_periodicidade
        maior_periodicidade = tabua_maior_periodicidade.periodicidade
        menor_periodicidade = tabua_menor_periodicidade.periodicidade
        tempo_menor_periodicidade = tabua_menor_periodicidade.tempo_futuro_maximo([0])
        tempo_maior_periodicidade = tabua_maior_periodicidade.tempo_futuro_maximo([0])
        assert tempo_menor_periodicidade - 1 == converter_periodicidade(
            tempo_maior_periodicidade - 1, maior_periodicidade, menor_periodicidade
        ).item()

    def test_aumentar_periodicidade_preserva_tpx_nos_pontos_de_quebra(self, aumentar_periodicidade):
        tabua_menor_periodicidade, tabua_maior_periodicidade = aumentar_periodicidade
        maior_periodicidade = tabua_maior_periodicidade.periodicidade
        menor_periodicidade = tabua_menor_periodicidade.periodicidade
        tempos_maior_periodicidade = arange(tabua_maior_periodicidade.tempo_futuro_maximo([0]))
        tempos_menor_periodicidade = converter_periodicidade(
            tempos_maior_periodicidade, maior_periodicidade, menor_periodicidade
        )
        assert all(mod(tempos_menor_periodicidade, 1) == 0)
        assert_array_almost_equal(
            tabua_maior_periodicidade.tpx([0], tempos_maior_periodicidade),
            tabua_menor_periodicidade.tpx([0], tempos_menor_periodicidade.astype(int))
        )

    def test_reduzir_periodicidade_preserva_tpx_nos_pontos_de_quebra(self, reduzir_periodicidade):
        tabua_menor_periodicidade, tabua_maior_periodicidade = reduzir_periodicidade
        maior_periodicidade = tabua_maior_periodicidade.periodicidade
        menor_periodicidade = tabua_menor_periodicidade.periodicidade
        tempos_maior_periodicidade = arange(tabua_maior_periodicidade.tempo_futuro_maximo([0]))
        tempos_menor_periodicidade = converter_periodicidade(
            tempos_maior_periodicidade, maior_periodicidade, menor_periodicidade
        )
        assert all(mod(tempos_menor_periodicidade, 1) == 0)
        assert_array_almost_equal(
            tabua_maior_periodicidade.tpx([0], tempos_maior_periodicidade),
            tabua_menor_periodicidade.tpx([0], tempos_menor_periodicidade.astype(int))
        )

    def test_aumentar_periodicidade_preserva_soma_de_t_qx_no_mesmo_periodo(self, aumentar_periodicidade):
        tabua_menor_periodicidade, tabua_maior_periodicidade = aumentar_periodicidade
        maior_periodicidade = tabua_maior_periodicidade.periodicidade
        menor_periodicidade = tabua_menor_periodicidade.periodicidade
        tempos_maior_periodicidade = arange(tabua_maior_periodicidade.tempo_futuro_maximo([0]))
        tempos_menor_periodicidade = arange(tabua_menor_periodicidade.tempo_futuro_maximo([0]))
        assert all(mod(tempos_menor_periodicidade, 1) == 0)
        pontos_split = converter_periodicidade(
            tempos_maior_periodicidade, maior_periodicidade, menor_periodicidade
        )[1:]
        assert all(mod(pontos_split, 1) == 0)
        tempos_splitted = split(tempos_menor_periodicidade, pontos_split.astype(int))
        t_qx_maior_periodicidade = tabua_maior_periodicidade.t_qx([0], tempos_maior_periodicidade)
        t_qx_menor_periodicidade = fromiter(
            map(lambda x: tabua_menor_periodicidade.t_qx([0], x).sum(), tempos_splitted), dtype=float
        )
        assert_array_almost_equal(
            t_qx_maior_periodicidade,
            t_qx_menor_periodicidade
        )

    def test_reduzir_periodicidade_preserva_soma_de_t_qx_no_mesmo_periodo(self, reduzir_periodicidade):
        tabua_menor_periodicidade, tabua_maior_periodicidade = reduzir_periodicidade
        maior_periodicidade = tabua_maior_periodicidade.periodicidade
        menor_periodicidade = tabua_menor_periodicidade.periodicidade
        tempos_maior_periodicidade = arange(tabua_maior_periodicidade.tempo_futuro_maximo([0]))
        tempos_menor_periodicidade = arange(tabua_menor_periodicidade.tempo_futuro_maximo([0]))
        assert all(mod(tempos_menor_periodicidade, 1) == 0)
        pontos_split = converter_periodicidade(
            tempos_maior_periodicidade, maior_periodicidade, menor_periodicidade
        )[1:]
        assert all(mod(pontos_split, 1) == 0)
        tempos_splitted = split(tempos_menor_periodicidade, pontos_split.astype(int))
        t_qx_maior_periodicidade = tabua_maior_periodicidade.t_qx([0], tempos_maior_periodicidade)
        t_qx_menor_periodicidade = fromiter(
            map(lambda x: tabua_menor_periodicidade.t_qx([0], x).sum(), tempos_splitted), dtype=float
        )
        assert_array_almost_equal(
            t_qx_maior_periodicidade,
            t_qx_menor_periodicidade
        )


class TestEfeitoAgravoNaTabua:
    def test_desagravar_qx_preserva_o_tempo_futuro_max(self):
        qx_original = array([0.1, 0.3, 0.5, 1.0])
        qx_agravado = agravar_qx(qx_original, percentual=50)
        tabua_original = Tabua(qx_original)
        tabua_agravada = Tabua(qx_agravado)
        assert tabua_original.tempo_futuro_maximo([0]) == tabua_agravada.tempo_futuro_maximo([0])

    def test_agravar_uma_tabua_pode_diminuir_o_tempo_futuro_maximo(self):
        qx_original = array([0.1, 0.3, 0.5, 1.0])
        qx_agravado = agravar_qx(qx_original, percentual=300)
        tabua_original = Tabua(qx_original)
        tabua_agravada = Tabua(qx_agravado)
        assert tabua_original.tempo_futuro_maximo([0]) > tabua_agravada.tempo_futuro_maximo([0])

    def test_agravar_uma_tabua_pode_nao_alterar_o_tempo_futuro_maximo(self):
        qx_original = array([0.1, 0.3, 0.5, 1.0])
        qx_agravado = agravar_qx(qx_original, percentual=110)
        tabua_original = Tabua(qx_original)
        tabua_agravada = Tabua(qx_agravado)
        assert tabua_original.tempo_futuro_maximo([0]) == tabua_agravada.tempo_futuro_maximo([0])
