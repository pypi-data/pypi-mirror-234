from numpy import array

from tabatu.periodicidade import Periodicidade
from tabatu.tabua_base import TabuaBase


def valida_periodicidade(*args: TabuaBase) -> Periodicidade:
    periodicidade = array([tabua.periodicidade for tabua in args])
    if not (periodicidade == periodicidade[0]).all():
        raise ValueError("Todas as tabuas precisam possuir a mesma periodicidade.")
    return periodicidade[0]
