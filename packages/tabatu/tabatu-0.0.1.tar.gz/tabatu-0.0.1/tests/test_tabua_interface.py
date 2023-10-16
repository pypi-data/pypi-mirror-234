from unittest.mock import Mock

import pytest

from tabatu.tabua_interface import valida_periodicidade
from tabatu.periodicidade import Periodicidade


def test_valida_periodicidade_falha_quando_recebe_tabuas_com_diferentes_periodicidades():
    tabua1 = Mock()
    tabua1.periodicidade = Periodicidade.MENSAL
    tabua2 = Mock()
    tabua2.periodicidade = Periodicidade.ANUAL
    with pytest.raises(ValueError):
        valida_periodicidade(tabua1, tabua2)


def test_valida_periodicidade_retorna_uma_unica_periodicidade_quando_todas_sao_iguais():
    tabua1 = Mock()
    tabua1.periodicidade = Periodicidade.MENSAL
    tabua2 = Mock()
    tabua2.periodicidade = Periodicidade.MENSAL
    assert valida_periodicidade(tabua1, tabua2) == Periodicidade.MENSAL
