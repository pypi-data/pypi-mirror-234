#pragma once
#include <vector>
#include "TabuaBaseCpp.h"
#include "TabuaInterfaceCpp.h"

class TabuaCpp final : public TabuaInterfaceCpp
{
private:
    std::vector<TabuaBaseCpp> m_tabuas;
    int m_numero_vidas = 1;
    int m_numero_decrementos = 1;

public:
    TabuaCpp();
    TabuaCpp(std::vector<double> qx);
    TabuaCpp(TabuaBaseCpp tabua);
    double qx(std::vector<int> x, double t) const;
    double tpx(std::vector<int> x, double t) const;
    std::vector<double> qx(std::vector<int> x, std::vector<double> t) const;
    std::vector<double> tpx(std::vector<int> x, std::vector<double> t) const;
    double tempo_futuro_maximo(std::vector<int> x) const;
};

std::vector<TabuaBaseCpp> extrairTabuasBase(std::vector<TabuaCpp> tabuas);