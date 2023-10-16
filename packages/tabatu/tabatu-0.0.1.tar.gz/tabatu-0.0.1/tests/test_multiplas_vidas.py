from unittest.mock import Mock

import pytest
from numpy import array, cumprod
from numpy.testing import assert_array_equal

from tabatu.multiplas_vidas import TabuaMultiplasVidas, StatusVidasConjuntas


def test_tpx_retorna_produto_acumulado_de_um_menos_qx(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMultiplasVidas(tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.LAST)
    assert tabua.tpx([0, 0], [0]) == 1
    assert_array_equal(tabua.tpx([0, 0], [1, 2, 3]), cumprod(1 - tabua.qx([0, 0], [0, 1, 2])))


def test_qx_retorna_o_produto_de_qx_de_cada_tabua_quando_status_eh_last(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMultiplasVidas(tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.LAST)
    resultado = tabua.qx([0, 0], [1, 2, 3])
    esperado = tabua_1dt_1.tabuas[0].qx(0, [1, 2, 3]) * tabua_1dt_2.tabuas[0].qx(0, [1, 2, 3])
    assert_array_equal(resultado, esperado)


def test_qx_retorna_um_menos_o_produto_de_1_menos_qx_quando_status_eh_joint(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMultiplasVidas(tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.JOINT)
    resultado = tabua.qx([0, 0], [1, 2, 3])
    esperado = 1 - (1 - tabua_1dt_1.tabuas[0].qx(0, [1, 2, 3])) * (1 - tabua_1dt_2.tabuas[0].qx(0, [1, 2, 3]))
    assert_array_equal(resultado, esperado)


def test_qx_falha_quando_tamanho_de_x_eh_incompativel_com_a_qntd_de_tabuas(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMultiplasVidas(tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.JOINT)
    with pytest.raises(ValueError):
        tabua.qx([0], [1, 2, 3])
    with pytest.raises(ValueError):
        tabua.qx([0, 0, 0], [1, 2, 3])


def test_tempo_futuro_max_retorna_o_menor_dos_tempos_quando_status_eh_joint(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMultiplasVidas(tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.JOINT)
    assert tabua.tempo_futuro_maximo([0, 0]) == min(
        tabua_1dt_1.tabuas[0].tempo_futuro_maximo(0),
        tabua_1dt_2.tabuas[0].tempo_futuro_maximo(0)
    )


def test_tempo_futuro_max_retorna_o_maior_dos_tempos_quando_status_eh_last(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMultiplasVidas(tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.LAST)
    assert tabua.tempo_futuro_maximo([0, 0]) == max(
        tabua_1dt_1.tabuas[0].tempo_futuro_maximo(0),
        tabua_1dt_2.tabuas[0].tempo_futuro_maximo(0)
    )


def test_tempo_futuro_max_falha_quando_o_tamanho_de_x_eh_incompativel_com_a_qntd_de_tabuas(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMultiplasVidas(tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.LAST)
    with pytest.raises(ValueError):
        tabua.tempo_futuro_maximo([0])
    with pytest.raises(ValueError):
        tabua.tempo_futuro_maximo([0, 0, 0])
