from enum import Enum

from numpy import atleast_1d, ndarray
from numpy.typing import ArrayLike


class Periodicidade(Enum):
    DIARIA = "DIARIA"
    SEMANAL = "SEMANAL"
    QUINZENAL = "QUINZENAL"
    MENSAL = "MENSAL"
    BIMESTRAL = "BIMESTRAL"
    TRIMESTRAL = "TRIMESTRAL"
    QUADRIMESTRAL = "QUADRIMESTRAL"
    SEMESTRAL = "SEMESTRAL"
    ANUAL = "ANUAL"

    def quantidade_periodos_1_ano(self) -> int:
        chaves = {
            Periodicidade.DIARIA: 365,
            Periodicidade.SEMANAL: 48,
            Periodicidade.QUINZENAL: 24,
            Periodicidade.MENSAL: 12,
            Periodicidade.BIMESTRAL: 6,
            Periodicidade.TRIMESTRAL: 4,
            Periodicidade.QUADRIMESTRAL: 3,
            Periodicidade.SEMESTRAL: 2,
            Periodicidade.ANUAL: 1,
        }
        return chaves[self]

    def quantidade_periodos_1_periodicidade(self, periodicidade):
        return (
            self.quantidade_periodos_1_ano() / periodicidade.quantidade_periodos_1_ano()
        )

    def __lt__(self, other):
        return self.quantidade_periodos_1_ano() > other.quantidade_periodos_1_ano()

    def __gt__(self, other):
        return self.quantidade_periodos_1_ano() < other.quantidade_periodos_1_ano()

    def __le__(self, other):
        return self.quantidade_periodos_1_ano() >= other.quantidade_periodos_1_ano()

    def __ge__(self, other):
        return self.quantidade_periodos_1_ano() <= other.quantidade_periodos_1_ano()


def converter_periodicidade(
    tempo: ArrayLike, periodicidade: Periodicidade, nova_periodicidade: Periodicidade
) -> ndarray[float]:
    tempo = atleast_1d(tempo)
    if nova_periodicidade == periodicidade:
        return tempo
    return tempo * nova_periodicidade.quantidade_periodos_1_periodicidade(periodicidade)


def meses2periodicidade(
    valor: ArrayLike, periodicidade: Periodicidade
) -> ndarray[float]:
    return converter_periodicidade(valor, Periodicidade.MENSAL, periodicidade)


def periodicidade2meses(valor: ArrayLike, periodicidade: Periodicidade) -> ndarray[int]:
    return converter_periodicidade(valor, periodicidade, Periodicidade.MENSAL).astype(
        int
    )
