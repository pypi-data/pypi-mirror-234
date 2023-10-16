#pragma once
#include <vector>
#include "TabuaBaseCpp.h"

class TabuaInterfaceCpp
{
private:
    int m_numero_decrementos;
    int m_numero_vidas;
    std::vector<TabuaBaseCpp> m_tabuas;

public:
    TabuaInterfaceCpp();
    TabuaInterfaceCpp(int numero_decrementos, int numero_vidas, std::vector<TabuaBaseCpp> tabuas);
    virtual double qx(std::vector<int> x, double t) const = 0;
    virtual double tpx(std::vector<int> x, double t) const = 0;
    virtual double tempo_futuro_maximo(std::vector<int> x) const = 0;
    bool possui_fechamento_plato() const;
    double t_qx(std::vector<int> x, double t) const;
    std::vector<double> t_qx(std::vector<int> x, std::vector<double> t) const;
    int pega_numero_vidas() const;
    int pega_numero_decrementos() const;
    std::vector<TabuaBaseCpp> pega_tabuas() const;
};