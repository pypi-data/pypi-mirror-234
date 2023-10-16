#pragma once
#include <vector>
#include "TabuaBaseCpp.h"
#include "TabuaCpp.h"
#include "TabuaInterfaceCpp.h"


enum class StatusVidasConjuntasCpp { JOINT, LAST };

class TabuaMultiplasVidasCpp final : public TabuaInterfaceCpp
{
private:
    std::vector<TabuaBaseCpp> m_tabuas;
    int m_numero_vidas = 1;
    int m_numero_decrementos = 1;
    StatusVidasConjuntasCpp m_status_vidas_conjuntas;

public:
    TabuaMultiplasVidasCpp();
    TabuaMultiplasVidasCpp(std::vector<TabuaCpp> tabuas, StatusVidasConjuntasCpp status_vidas_conjuntas);
    double qx(std::vector<int> x, double t) const;
    double tpx(std::vector<int> x, double t) const;
    std::vector<double> qx(std::vector<int> x, std::vector<double> t) const;
    std::vector<double> tpx(std::vector<int> x, std::vector<double> t) const;
    double tempo_futuro_maximo(std::vector<int> x) const;
};