#include "TabuaMultiplasVidasCpp.h"
#include "TabuaCpp.h"
#include <stdexcept>
#include <cmath>
#include <algorithm>


TabuaMultiplasVidasCpp::TabuaMultiplasVidasCpp() : TabuaInterfaceCpp() {
}

TabuaMultiplasVidasCpp::TabuaMultiplasVidasCpp(std::vector<TabuaCpp> tabuas, StatusVidasConjuntasCpp status_vidas_conjuntas) :
	TabuaInterfaceCpp(1, (int)tabuas.size(), extrairTabuasBase(tabuas))
{
	m_numero_vidas = (int)tabuas.size();
	m_tabuas = extrairTabuasBase(tabuas);
	m_status_vidas_conjuntas = status_vidas_conjuntas;
}


double TabuaMultiplasVidasCpp::qx(std::vector<int> x, double t) const {
	if (x.size() != m_numero_vidas) {
		throw std::invalid_argument("x deve ser um vetor com tamanho igual ao numero de vidas.");
	}
	double ret = 1.0;
	if (m_status_vidas_conjuntas == StatusVidasConjuntasCpp::JOINT) {
		for (size_t i = 0; i < m_numero_vidas; i++)
		{
			ret = ret * (1 - m_tabuas[i].qx(x[i], t));
		}
		return 1 - ret;
	}
	for (size_t i = 0; i < m_numero_vidas; i++)
	{
		ret = ret * m_tabuas[i].qx(x[i], t);
	}
	return ret;

}

double TabuaMultiplasVidasCpp::tpx(std::vector<int> x, double t) const {
	if (x.size() != m_numero_vidas) {
		throw std::invalid_argument("x deve ser um vetor com tamanho igual ao numero de vidas.");
	}

	if (m_status_vidas_conjuntas == StatusVidasConjuntasCpp::JOINT) {
		double ret = 1.0;
		for (size_t i = 0; i < m_numero_vidas; i++)
		{
			ret = ret * m_tabuas[i].tpx(x[i], t);
		}
		return ret;
	}
	for (size_t i = 0; i < m_numero_vidas; i++)
	{
		if (x[i] < 0) {
			throw std::invalid_argument("x deve ser maior ou igual a 0");
		}
	}
	if (t < 0) {
		throw std::invalid_argument("t deve ser maior ou igual a 0");
	}
	double lx_t;
	lx_t = 1.0;
	for (size_t i = 1; i <= (int)t; i++)
	{
		lx_t = lx_t * (1 - qx(x, (double)(i - 1)));
	}
	return lx_t;
}

std::vector<double> TabuaMultiplasVidasCpp::qx(std::vector<int> x, std::vector<double> t) const {
	std::vector<double> ret(t.size());
	int n = (int)t.size();
	for (int i = 0; i < n; i++)
	{
		ret[i] = qx(x, t[i]);
	}
	return ret;
}

std::vector<double> TabuaMultiplasVidasCpp::tpx(std::vector<int> x, std::vector<double> t) const {
	std::vector<double> ret(t.size());
	int n = (int)t.size();
	for (int i = 0; i < n; i++)
	{
		ret[i] = tpx(x, t[i]);
	}
	return ret;
}

double TabuaMultiplasVidasCpp::tempo_futuro_maximo(std::vector<int> x) const {
	if (x.size() != m_numero_vidas) {
		throw std::invalid_argument("x deve ser um vetor com tamanho igual ao numero de vidas.");
	}
	std::vector<double> ret(m_numero_vidas);
	for (size_t i = 0; i < m_numero_vidas; i++)
	{
		ret[i] = m_tabuas[i].tempo_futuro_maximo(x[i]);
	}
	if (m_status_vidas_conjuntas == StatusVidasConjuntasCpp::JOINT) {
		return *std::min_element(ret.begin(), ret.end());
	}
	return *std::max_element(ret.begin(), ret.end());
}


