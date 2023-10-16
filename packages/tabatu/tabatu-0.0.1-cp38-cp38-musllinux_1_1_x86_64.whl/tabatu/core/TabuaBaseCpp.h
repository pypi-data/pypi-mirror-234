#pragma once
#include <vector>
#include <limits>


class TabuaBaseCpp final
{
private:
    std::vector<double> m_qx;
    std::vector<double> m_lx;
    double m_w = std::numeric_limits<double>::infinity();
    int m_qx_size;

public:
    TabuaBaseCpp();
    TabuaBaseCpp(std::vector<double> qx);
    double qx(int x, double t) const;
    double tpx(int x, double t) const;
    double t_qx(int x, double t) const;
    std::vector<double> qx(int x, std::vector<double> t) const;
    std::vector<double> tpx(int x, std::vector<double> t) const;
    std::vector<double> t_qx(int x, std::vector<double> t) const;
    double tempo_futuro_maximo(int x) const;
    bool possui_fechamento_plato() const;
    std::vector<double> pega_qx() const;

private:
    double lx(double x) const;
    void calcular_lx(double raiz);
};