from libcpp.vector cimport vector
from TabuaInterfaceCpp cimport TabuaInterfaceCpp

cdef extern from "TabuaCpp.cpp":
    pass

cdef extern from "TabuaCpp.h":
    cdef cppclass TabuaCpp(TabuaInterfaceCpp):
        TabuaCpp() except +
        TabuaCpp(vector[double] qx)
        vector[double] qx(vector[int] x, vector[double] t) except +
        vector[double] tpx(vector[int] x, vector[double] t) except +
        double tempo_futuro_maximo(vector[int] x) except +
