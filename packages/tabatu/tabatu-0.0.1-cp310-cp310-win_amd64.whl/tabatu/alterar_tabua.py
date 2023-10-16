from numpy import append
from numpy import apply_along_axis
from numpy import arange
from numpy import atleast_1d
from numpy import minimum
from numpy import multiply
from numpy import ndarray
from numpy import ones_like
from numpy import repeat
from numpy import split
from numpy.typing import ArrayLike

from tabatu.periodicidade import Periodicidade


def _all_equal(arr: ArrayLike) -> bool:
    """Verifica se todos os elementos de um array são iguais."""
    arr = atleast_1d(arr)
    return all(arr == arr[0])


def _reduzir_periodicidade(
    qx: ndarray[float], periodicidade: Periodicidade, nova_periodicidade: Periodicidade
) -> ndarray[float]:
    """Aumenta a periodicidade ao repetir os valores de qx para cada subintervalo e alterá-los.
    Por exemplo, quando o qx é anual e queremos reduzir para mensal, o qx de cada ano é repetido 12 vezes e
    alterado para o qx mensal. Dessa forma, o qx de cada mes em um mesmo ano será igual."""
    razao_periodicidade = nova_periodicidade.quantidade_periodos_1_periodicidade(periodicidade)
    if not razao_periodicidade.is_integer():
        raise ValueError(
            f"A quantidade de periodos da nova periodicidade em 1 período da periodicidade original deve ser inteiro."
            f" Por exemplo, em um trimestre existem 1.5 bimestres, logo, não é possível converter."
        )
    qx_explodido = repeat(qx, int(razao_periodicidade))
    return 1 - (1 - qx_explodido) ** (1 / razao_periodicidade)


def _aumentar_periodicidade(
    qx: ndarray[float], periodicidade: Periodicidade, nova_periodicidade: Periodicidade
) -> ndarray[float]:
    step = periodicidade.quantidade_periodos_1_periodicidade(nova_periodicidade)
    if not step.is_integer():
        raise ValueError(
            f"A quantidade de periodos da periodicidade em 1 período da nova periodicidade original deve ser inteiro."
            f" Por exemplo, em um trimestre existem 1.5 bimestres, logo, não é possível converter."
        )
    step = int(step)
    if len(qx) % step != 0:
        adicionar = repeat(qx[-1], len(qx) % step)
        qx = append(qx, adicionar)
    pontos_split = arange(step, len(qx), step)
    qx_splitado = split(qx, pontos_split)
    elementos_de_cada_array_sao_iguais = apply_along_axis(_all_equal, 1, qx_splitado)
    if not all(elementos_de_cada_array_sao_iguais):
        raise ValueError(
            "Alterar a periodicidade de uma tábua que não possui taxas constantes em cada subintervalo"
            " resultaria em perda de informação."
        )
    qx_reduzido = qx[0:len(qx):step]
    return 1 - (1 - qx_reduzido) ** step


def alterar_periodicidade_qx(
    qx: ndarray[float], periodicidade: Periodicidade, nova_periodicidade: Periodicidade
) -> ndarray[float]:
    """Altera a periodicidade de um array de taxas. Retorna um novo array de taxas.

    IMPORTANTE: As taxas devem ser agravadas antes de terem a sua periodicidade alterada."""
    if periodicidade > nova_periodicidade:
        return _reduzir_periodicidade(qx, periodicidade, nova_periodicidade)
    if periodicidade < nova_periodicidade:
        return _aumentar_periodicidade(qx, periodicidade, nova_periodicidade)
    return qx


def agravar_qx(qx: ndarray[float], percentual: float) -> ndarray[float]:
    if percentual < 0:
        raise ValueError("O percentual deve ser positivo.")
    qx = minimum(multiply(qx, percentual / 100, out=ones_like(qx), where=qx < 1), 1)
    return qx
