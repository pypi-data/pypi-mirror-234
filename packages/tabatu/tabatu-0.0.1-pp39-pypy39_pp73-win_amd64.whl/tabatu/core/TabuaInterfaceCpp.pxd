from libcpp.vector cimport vector
from libcpp cimport bool
from TabuaBaseCpp cimport TabuaBaseCpp

cdef extern from "TabuaInterfaceCpp.cpp":
    pass

cdef extern from "TabuaInterfaceCpp.h":
    cdef cppclass TabuaInterfaceCpp:
        TabuaInterfaceCpp() except +
        TabuaInterfaceCpp(int numero_decrementos, int numero_vidas, vector[TabuaBaseCpp] tabuas)
        bool possui_fechamento_plato() const
        vector[double] t_qx(vector[int] x, vector[double] t) except +
        int pega_numero_vidas() const
        int pega_numero_decrementos() const
        vector[TabuaBaseCpp] pega_tabuas() const