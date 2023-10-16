from __future__ import annotations

from enum import Enum
from typing import Iterable

from numpy import ndarray

import tabatu.core as core
from tabatu.tabua_interface import valida_periodicidade
from tabatu.unico_decremento import Tabua


class StatusVidasConjuntas(Enum):
    JOINT = b"JOINT"
    LAST = b"LAST"


class TabuaMultiplasVidas(core.TabuaMultiplasVidas):
    __slots__ = "_periodicidade", "_status"

    def __init__(self, *args: Tabua, status: StatusVidasConjuntas = StatusVidasConjuntas.LAST) -> None:
        self._periodicidade = valida_periodicidade(*args)
        self._status = status
        super().__init__(*args, status=core.StatusVidasConjuntas(status.value))

    @property
    def status(self) -> StatusVidasConjuntas:
        """Status de vida conjunta."""
        return self._status

    def qx(self, x: Iterable[int], t: Iterable[int]) -> ndarray[float]:
        """Probabilidade de falha entre as idades x + t e x + t + 1.

        A falha é definida pelo status da tabua. Se o status é "last", então
        a falha é definida por todas as vidas falharem.
        Se o status é "joint", então a falha é definida por pelo menos uma vida
        falhar.

        Args:
            x (Iterable[int]): Idade de inicial. Deve ser um array com 1 elemento
                para cada vida.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Array com o mesmo tamanho que t, fornecendo as probabilidades
            de falha entre x + t e x + t + 1.

        Examples:

            Como seria esperado, as probabildiades de falha no status "last"
            são mais baixas que as probabilidades de falha no status "joint".

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> tabua = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status=StatusVidasConjuntas.LAST)
            >>> tabua.qx([50, 30], [0, 1, 2, 3])
            array([0.1581, 0.1664, 0.1749, 0.1836])
            >>> tabua = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status=StatusVidasConjuntas.JOINT)
            >>> tabua.qx([50, 30], [0, 1, 2, 3])
            array([0.6619, 0.6736, 0.6851, 0.6964])
        """
        return super().qx(x, t)

    def tpx(self, x: Iterable[int], t: Iterable[int]) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x sobreviver a idade
        x + t.

        Args:
            x (Iterable[int]): Idade de inicial. Deve ser um array com 1 elemento
                para cada vida.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Probabilidade de um indivíduo com idade x sobreviver a
            idade x + t.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100

            >>> tabua = TabuaMultiplasVidas(Tabua(qx), Tabua(qx), status = StatusVidasConjuntas.LAST)
            >>> tpx = tabua.tpx([30, 50], [0,1,2,3,4,5])
            >>> np.round(tpx, 5)
            array([1.     , 0.8419 , 0.70181, 0.57906, 0.47275, 0.38174])
        """
        return super().tpx(x, t)

    def t_qx(self, x: Iterable[int], t: Iterable[int]) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x falhar com
        idade exatamente igual a x + t.

        Args:
            x (Iterable[int]): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Probabilidade de um indivíduo com idade x falhar com
            idade exatamente igual a x + t.
        """
        return super().t_qx(x, t)

    def tempo_futuro_maximo(self, x: Iterable[int]) -> float:
        """Tempo de vida futuro máximo.

        A idade deve ser composta por um array com tamanho igual ao número de vidas.

        Args:
            x (Iterable[int]): Idade de inicial. Deve ser um array com
                uma idade para cada vida.

        Returns:
            float: Tempo de vida futuro máximo, pode ser infinito.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100

            Com o status "last" o tempo futuro é maior dos tempos, afinal a tabua
            continua se pelo menos uma vida está viva.

            >>> tabua = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status = StatusVidasConjuntas.LAST)
            >>> tabua.tempo_futuro_maximo([50, 30])
            70.0

            Já para o status "joint", quando a primeira vida morre, a tabua se encerra.

            >>> tabua = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status = StatusVidasConjuntas.JOINT)
            >>> tabua.tempo_futuro_maximo([50, 30])
            50.0
        """
        return super().tempo_futuro_maximo(x)

    def possui_fechamento_plato(self) -> bool:
        """Verifica se a tábua possui fechamento de tipo platô."""
        return super().possui_fechamento_plato()
