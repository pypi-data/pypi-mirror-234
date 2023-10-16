#include "TabuaCpp.h"
#include "TabuaBaseCpp.h"
#include <stdexcept>

std::vector<TabuaBaseCpp> extrairTabuasBase(std::vector<TabuaCpp> tabuas) {
	std::vector<TabuaBaseCpp> tabuasBase;
	tabuasBase.reserve(tabuas.size());
	for (TabuaCpp tabua : tabuas) {
		tabuasBase.push_back(tabua.pega_tabuas()[0]);
	}
	return tabuasBase;
}

TabuaCpp::TabuaCpp() : TabuaInterfaceCpp() {
}

TabuaCpp::TabuaCpp(std::vector<double> qx) : TabuaInterfaceCpp(1, 1, { TabuaBaseCpp(qx) })
{
    m_tabuas = { TabuaBaseCpp(qx) };
}

TabuaCpp::TabuaCpp(TabuaBaseCpp tabua) : TabuaInterfaceCpp(1, 1, { tabua })
{
    m_tabuas = { tabua };
}

double TabuaCpp::qx(std::vector<int> x, double t) const {
    return m_tabuas[0].qx(x[0], t);
}

double TabuaCpp::tpx(std::vector<int> x, double t) const {
    return m_tabuas[0].tpx(x[0], t);
}

std::vector<double> TabuaCpp::qx(std::vector<int> x, std::vector<double> t) const {
    if (x.size() > 1) {
        throw std::invalid_argument("x deve ter tamanho 1");
    }
    return m_tabuas[0].qx(x[0], t);
}

std::vector<double> TabuaCpp::tpx(std::vector<int> x, std::vector<double> t) const {
    if (x.size() > 1) {
        throw std::invalid_argument("x deve ter tamanho 1");
    }
    return m_tabuas[0].tpx(x[0], t);
}

double TabuaCpp::tempo_futuro_maximo(std::vector<int> x) const {
    if (x.size() > 1) {
        throw std::invalid_argument("x deve ter tamanho 1");
    }
    return m_tabuas[0].tempo_futuro_maximo(x[0]);
}




