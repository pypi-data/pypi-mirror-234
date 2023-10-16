#pragma once
#include <vector>
#include "TabuaBaseCpp.h"
#include "TabuaCpp.h"
#include "TabuaInterfaceCpp.h"

class TabuaMDTCpp final : public TabuaInterfaceCpp
{
private:
    int m_numero_decrementos;
    int m_numero_vidas = 1;
    std::vector<TabuaBaseCpp> m_tabuas;
public:
    TabuaMDTCpp();
    TabuaMDTCpp(std::vector<TabuaCpp> tabuas);
    double qx_j(std::vector<int> x, double t, int j) const;
    double qx(std::vector<int> x, double t) const;
    double tpx(std::vector<int> x, double t) const;
    std::vector<double> qx_j(std::vector<int> x, std::vector<double> t, int j) const;
    std::vector<std::vector<double>> qx_j(std::vector<int> x, std::vector<double> t, std::vector<int> j) const;
    std::vector<double> qx(std::vector<int> x, std::vector<double> t) const;
    std::vector<double> tpx(std::vector<int> x, std::vector<double> t) const;
    std::vector<double> t_qx_j(std::vector<int> x, std::vector<double> t, int j) const;
    std::vector<std::vector<double>> t_qx_j(std::vector<int> x, std::vector<double> t, std::vector<int> j) const;
    double tempo_futuro_maximo(std::vector<int> x) const;
};