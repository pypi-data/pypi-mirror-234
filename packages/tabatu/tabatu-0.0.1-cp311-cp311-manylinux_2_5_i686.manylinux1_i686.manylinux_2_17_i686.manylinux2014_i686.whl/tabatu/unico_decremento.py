from __future__ import annotations

from typing import Iterable

from tabatu.periodicidade import Periodicidade
from numpy import ndarray

import tabatu.core as core


class Tabua(core.Tabua):
    __slots__ = "_periodicidade"

    def __init__(
        self, qx: ndarray[float], periodicidade: Periodicidade = Periodicidade.ANUAL
    ):
        super().__init__(qx)
        self._periodicidade = periodicidade

    @property
    def periodicidade(self) -> Periodicidade:
        """Periodicidade da tábua."""
        return self._periodicidade

    def qx(self, x: Iterable[int], t: Iterable[int]) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x + t falhar
        antes de completar a idade x + t + 1.

        Args:
            x (Iterable[int]): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Array com o mesmo tamanho que t, fornecendo as probabilidades
            de falha entre x + t e x + t + 1.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).qx([30], [0,1,2,3,4,5])
            array([0.31, 0.32, 0.33, 0.34, 0.35, 0.36])
        """
        return super().qx(x, t)

    def tpx(self, x: Iterable[int], t: Iterable[int]) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x sobreviver a idade
        x + t.

        Args:
            x (Iterable[int]): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Probabilidade de um indivíduo com idade x sobreviver a
            idade x + t.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).tpx([30], [0,1,2,3,4,5])
            array([1.        , 0.69      , 0.4692    , 0.314364  , 0.20748024,
                   0.13486216])
        """
        return super().tpx(x, t)

    def t_qx(self, x: Iterable[int], t: Iterable[int]) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x falhar com
        idade exatamente igual a x + t.

        Args:
            x (Iterable[int]): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Probabilidade de um indivíduo com idade x falhar com
            idade exatamente igual a x + t.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).t_qx([30], [0, 1, 2, 3, 4, 5])
            array([0.31      , 0.2208    , 0.154836  , 0.10688376, 0.07261808,
                   0.04855038])
        """
        return super().t_qx(x, t)

    def tempo_futuro_maximo(self, x: Iterable[int]) -> float:
        """Tempo de vida futuro máximo.

        Args:
            x (Iterable[int]): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.

        Returns:
            float: Tempo de vida futuro máximo, pode ser infinito.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).tempo_futuro_maximo([30])
            70.0
            >>> Tabua(qx).tempo_futuro_maximo([0])
            100.0
        """
        return super().tempo_futuro_maximo(x)

    def possui_fechamento_plato(self) -> bool:
        """Verifica se a tábua possui fechamento de tipo platô."""
        return super().possui_fechamento_plato()
