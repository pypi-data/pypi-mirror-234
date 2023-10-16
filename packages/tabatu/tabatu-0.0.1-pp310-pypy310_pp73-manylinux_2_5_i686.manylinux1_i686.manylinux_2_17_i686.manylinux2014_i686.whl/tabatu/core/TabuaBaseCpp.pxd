from libcpp.vector cimport vector
from libcpp cimport bool

cdef extern from "TabuaBaseCpp.cpp":
    pass

cdef extern from "TabuaBaseCpp.h":
    cdef cppclass TabuaBaseCpp:
        TabuaBaseCpp() except +
        TabuaBaseCpp(vector[double] qx)
        double qx(int x, double t) const
        double tpx(int x, double t) const
        double t_qx(int x, double t) const
        vector[double] qx(int x, vector[double] t) except +
        vector[double] tpx(int x, vector[double] t) except +
        vector[double] t_qx(int x, vector[double] t) except +
        double tempo_futuro_maximo(int x) except +
        bool possui_fechamento_plato() const
        vector[double] pega_qx() const
