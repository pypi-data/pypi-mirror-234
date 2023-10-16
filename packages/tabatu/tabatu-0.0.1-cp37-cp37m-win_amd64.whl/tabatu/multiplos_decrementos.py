from __future__ import annotations

from typing import Any
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import Union

from numpy import ndarray
from numpy.typing import ArrayLike

import tabatu.core as core
from tabatu.tabua_interface import valida_periodicidade
from tabatu.unico_decremento import Tabua


def captura_argumentos(*args: Any, **kwargs: Any) -> dict[str, int]:
    result = {}
    for i in range(len(args)):
        result[str(i)] = i
    contador = len(args)
    for key in kwargs.keys():
        result[key] = contador
        contador += 1
    return result


def valida_quantidade_tabuas(*args: Any) -> Any:
    if len(args) == 0:
        raise ValueError("Pelo menos 1 tábua deve ser fornecida.")
    if len(args) > 3:
        raise ValueError("São suportadas no máximo 3 tábuas.")
    return args


def valida_causa_principal(
    causa_principal: Union[int, str], causas: dict[str, int]
) -> Optional[str]:
    if causa_principal is None:
        return None
    if isinstance(causa_principal, int):
        causa_principal = str(causa_principal)
    if causa_principal not in causas.keys():
        raise ValueError(
            f"Causa principal invalida. Deve ser um entre {list(causas.keys())}."
        )
    return causa_principal


class TabuaMDT(core.TabuaMDT):
    __slots__ = "_periodicidade", "_causa_principal", "_causas"

    def __init__(
        self,
        *args: Tabua,
        causa_principal: Union[int, str, None] = None,
        **kwargs: Tabua,
    ) -> None:
        tabuas: tuple[Tabua, ...] = args + tuple(kwargs.values())
        tabuas = valida_quantidade_tabuas(*tabuas)
        self._causas = captura_argumentos(*args, **kwargs)
        self._causa_principal: Optional[str] = valida_causa_principal(
            causa_principal, self._causas
        )
        self._periodicidade = valida_periodicidade(*tabuas)
        super().__init__(*tabuas)

    @property
    def causas(self) -> dict[str, int]:
        return self._causas

    @property
    def causa_principal(self) -> Optional[str]:
        return self._causa_principal

    def possui_causa_principal(self) -> bool:
        """Verifica se existe uma causa principal."""
        return self._causa_principal is not None

    def qx_j(self, x: Iterable[int], t: Iterable[int], j: Sequence[int] | Sequence[str]) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x + t falhar pela causa j
        antes de completar a idade x + t + 1.

        Args:
            x (Iterable[int]): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.
            j (Iterable[int] or Iterable[str]): Causa da falha. Deve ser um número de 0 até self.n_decremento ou uma
                string com o nome da causa. Pode receber mais de um número. As causas de falha são ordenadas pela
                forma como foram utilizadas na inicialização da classe, e possuirão um nome igual à ordem em que foram
                passadas ou com o nome do argumento, caso tenha sido passada como argumento nomeado.

        Returns:
            ndarray[float]: Array com o mesmo tamanho que t, fornecendo as probabilidades
            de falha pela causa j entre x + t e x + t + 1.

        Notes:
            As probabilidades são convertidas para o cenário de múltiplos decrementos
            antes do cálculo.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), causa2=Tabua(qx2))
            >>> tabua.qx_j([50, 0], [0, 1, 2, 3], [0])
            array([[0.50745, 0.5174 , 0.52735, 0.5373 ]])
            >>> tabua.qx_j([50, 0], [0, 1, 2, 3], [1])
            array([[0.00745, 0.0074 , 0.00735, 0.0073 ]])
            >>> tabua.qx_j([50, 0], [0, 1, 2, 3], [0, 1])
            array([[0.50745, 0.5174 , 0.52735, 0.5373 ],
                   [0.00745, 0.0074 , 0.00735, 0.0073 ]])
            >>> tabua.qx_j([50, 0], [0, 1, 2, 3], ["0", "causa2"])
            array([[0.50745, 0.5174 , 0.52735, 0.5373 ],
                   [0.00745, 0.0074 , 0.00735, 0.0073 ]])
        """
        j = self._padronizar_j(j)
        return super().qx_j(x, t, j)

    def t_qx_j(self, x: Iterable[int], t: Iterable[int], j: Sequence[int] | Sequence[str]) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x falhar com
        idade exatamente igual a x + t, pela causa j.

        Args:
            x (Iterable[int]): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.
            j (Iterable[int] or Iterable[str]): Causa da falha. Deve ser um número de 0 até self.n_decremento ou uma
                string com o nome da causa. Pode receber mais de um número. As causas de falha são ordenadas pela
                forma como foram utilizadas na inicialização da classe, e possuirão um nome igual à ordem em que foram
                passadas ou com o nome do argumento, caso tenha sido passada como argumento nomeado.

        Returns:
            ndarray[float]: Probabilidade de um indivíduo com idade x falhar com
            idade exatamente igual a x + t, pela causa j.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), causa2=Tabua(qx2))
            >>> tabua.t_qx_j([50, 0], [0, 1, 2, 3], [0])
            array([[0.50745   , 0.25099074, 0.12156447, 0.05763119]])
            >>> tabua.t_qx_j([50, 0], [0, 1, 2, 3], [1])
            array([[0.00745   , 0.00358974, 0.00169432, 0.000783  ]])
            >>> tabua.t_qx_j([50, 0], [0, 1, 2, 3], [0, 1])
            array([[0.50745   , 0.25099074, 0.12156447, 0.05763119],
                   [0.00745   , 0.00358974, 0.00169432, 0.000783  ]])
            >>> tabua.t_qx_j([50, 0], [0, 1, 2, 3], ["0", "causa2"])
            array([[0.50745   , 0.25099074, 0.12156447, 0.05763119],
                   [0.00745   , 0.00358974, 0.00169432, 0.000783  ]])
        """
        j = self._padronizar_j(j)
        return super().t_qx_j(x, t, j)

    def qx(self, x: Iterable[int], t: Iterable[int]) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x + t falhar por qualquer causa
        antes de completar a idade x + t + 1.

        Args:
            x (Iterable[int]): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Array com o mesmo tamanho que t, fornecendo as probabilidades
            de falha entre x + t e x + t + 1.

        Notes:
            As probabilidades são convertidas para o cenário de múltiplos decrementos
            antes do cálculo.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), Tabua(qx2))
            >>> tabua.qx([50, 0], [0, 1, 2, 3])
            array([0.5149, 0.5248, 0.5347, 0.5446])
        """
        return super().qx(x, t)

    def tpx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x sobreviver a idade
        x + t.

        Args:
            x (ArrayLike): Idade de inicial. Deve ser um array com 1 elemento
                para cada decremento.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray: Probabilidade de um indivíduo com idade x sobreviver a
            idade x + t.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), Tabua(qx2))
            >>> tabua.tpx([30, 30], [0, 1, 2, 3])
            array([1.        , 0.6831    , 0.45986292, 0.30502707])
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
            idade exatamente igual a x + t. Se a tábua possui causa principal, então
            é a probabilidade de falhar pela causa principal. Se não possui causa principal,
            é a probabilidade de falhar por qualquer causa.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), Tabua(qx2))
            >>> tabua.t_qx([50, 0], [0, 1, 2, 3])
            array([0.5149    , 0.25458048, 0.12325879, 0.0584142 ])
        """
        if self._causa_principal is None:
            return super().t_qx(x, t)
        return self.t_qx_j(x, t, [self._causa_principal]).sum(axis=0)

    def tempo_futuro_maximo(self, x: Iterable[int]) -> float:
        """Tempo de vida futuro máximo.

        A idade pode ser composta de duas idades diferentes, como, por exemplo,
        no caso em que existe uma tábua de morte e uma tábua de cancelamento.

        Args:
            x (Iterable[int]): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.

        Returns:
            float: Tempo de vida futuro máximo, pode ser infinito.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), Tabua(qx2))
            >>> tabua.tempo_futuro_maximo([30, 30])
            70.0
            >>> tabua.tempo_futuro_maximo([50, 0])
            50.0
        """
        return super().tempo_futuro_maximo(x)

    def possui_fechamento_plato(self) -> bool:
        """Verifica se a tábua possui fechamento de tipo platô."""
        return super().possui_fechamento_plato()

    def _padronizar_j(self, j: Iterable[int]) -> list[int]:
        return [self._causas[x] if isinstance(x, str) else x for x in j]