from libcpp.vector cimport vector
from TabuaCpp cimport TabuaCpp
from TabuaInterfaceCpp cimport TabuaInterfaceCpp
cdef extern from "TabuaMultiplasVidasCpp.cpp":
    pass

cdef extern from "TabuaMultiplasVidasCpp.h":
    cdef cppclass TabuaMultiplasVidasCpp(TabuaInterfaceCpp):
        TabuaMultiplasVidasCpp() except +
        TabuaMultiplasVidasCpp(vector[TabuaCpp] tabuas, StatusVidasConjuntasCpp status_vidas_conjuntas)
        vector[double] qx(vector[int] x, vector[double] t) except +
        vector[double] tpx(vector[int] x, vector[double] t) except +
        double tempo_futuro_maximo(vector[int] x) except +


    cdef cppclass StatusVidasConjuntasCpp:
        pass



