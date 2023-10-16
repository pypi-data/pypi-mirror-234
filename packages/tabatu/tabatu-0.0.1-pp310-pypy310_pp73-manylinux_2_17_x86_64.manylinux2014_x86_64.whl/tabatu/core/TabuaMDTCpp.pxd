from libcpp.vector cimport vector
from TabuaCpp cimport TabuaCpp
from TabuaInterfaceCpp cimport TabuaInterfaceCpp

cdef extern from "TabuaMDTCpp.cpp":
    pass

cdef extern from "TabuaMDTCpp.h":
    cdef cppclass TabuaMDTCpp(TabuaInterfaceCpp):
        TabuaMDTCpp() except +
        TabuaMDTCpp(vector[TabuaCpp] tabuas)
        vector[vector[double]] qx_j(vector[int] x, vector[double] t, vector[int] j) except +
        vector[double] qx(vector[int] x, vector[double] t) except +
        vector[double] tpx(vector[int] x, vector[double] t) except +
        vector[vector[double]] t_qx_j(vector[int] x, vector[double] t, vector[int] j) except +
        double tempo_futuro_maximo(vector[int] x) except +

