#include "TabuaMDTCpp.h"
#include "TabuaCpp.h"
#include <stdexcept>
#include <cmath>
#include <algorithm>

double qx2qxj(double qx1, double qx2, double qx3)
{
	return qx1 * (1 - 0.5 * (qx2 + qx3) + 1.0 / 3.0 * (qx2 * qx3));
}

std::vector<double> qx2qxj(std::vector<double> qx1, std::vector<double> qx2, std::vector<double> qx3)
{
	std::vector<double> qxj;
	qxj.reserve(qx1.size());
	for (int i = 0; i < qx1.size(); i++)
	{
		qxj.push_back(qx2qxj(qx1[i], qx2[i], qx3[i]));
	}
	return qxj;
}

std::vector<double> converter_mdt(std::vector<double> qx) {
	std::vector<double> qxj(3);
	int tamanho = 3 - (int)qx.size();
	double zeros = 0.0;
	if (tamanho < 0) {
		throw std::invalid_argument("O número de tábuas não pode ser maior que 3");
	}
	for (int i = 0; i < tamanho; i++) {
		qx.push_back(zeros);
	}
	qxj[0] = qx2qxj(qx[0], qx[1], qx[2]);
	qxj[1] = qx2qxj(qx[1], qx[2], qx[0]);
	qxj[2] = qx2qxj(qx[2], qx[0], qx[1]);
	return qxj;
}

std::vector<std::vector<double>> converter_mdt(std::vector<std::vector<double>> qx) {
	std::vector<std::vector<double>> qxj(3);
	int tamanho = 3 - (int)qx.size();
	std::vector<double> zeros(qx[0].size(), 0.0);
	if (tamanho < 0) {
		throw std::invalid_argument("O número de tábuas não pode ser maior que 3");
	}
	for (int i = 0; i < tamanho; i++) {
		qx.push_back(zeros);
	}
	qxj[0] = qx2qxj(qx[0], qx[1], qx[2]);
	qxj[1] = qx2qxj(qx[1], qx[2], qx[0]);
	qxj[2] = qx2qxj(qx[2], qx[0], qx[1]);
	return qxj;
}

TabuaMDTCpp::TabuaMDTCpp() : TabuaInterfaceCpp() {
}

TabuaMDTCpp::TabuaMDTCpp(std::vector<TabuaCpp> tabuas) : TabuaInterfaceCpp((int)tabuas.size(), 1, extrairTabuasBase(tabuas))
{
	m_numero_decrementos = (int)tabuas.size();
	m_tabuas = extrairTabuasBase(tabuas);
}

// comeco
double TabuaMDTCpp::qx_j(std::vector<int> x, double t, int j) const {
	if (x.size() != m_numero_decrementos) {
		throw std::invalid_argument("x deve ser um vetor com tamanho igual ao numero de decrementos.");
	}
	if (j > m_numero_decrementos) {
		throw std::out_of_range("");
	}
	std::vector<double> qx;
	qx.reserve(m_tabuas.size());
	for (size_t i = 0; i < m_numero_decrementos; i++) {
		qx.push_back(m_tabuas[i].qx(x[i], t));
	}
	return converter_mdt(qx)[j];
}

std::vector<double> TabuaMDTCpp::qx_j(std::vector<int> x, std::vector<double> t, int j) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = qx_j(x, t[i], j);
    }
    return ret;
}

std::vector<std::vector<double>> TabuaMDTCpp::qx_j(std::vector<int> x, std::vector<double> t, std::vector<int> j) const {
    std::vector<std::vector<double>> ret(j.size());
    int n = (int)j.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = qx_j(x, t, j[i]);
    }
    return ret;
}

std::vector<double> TabuaMDTCpp::t_qx_j(std::vector<int> x, std::vector<double> t, int j) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = tpx(x, t[i]) * qx_j(x, t[i], j);
    }
    return ret;
}

std::vector<std::vector<double>> TabuaMDTCpp::t_qx_j(std::vector<int> x, std::vector<double> t, std::vector<int> j) const {
    std::vector<std::vector<double>> ret(j.size());
    int n = (int)j.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = t_qx_j(x, t, j[i]);
    }
    return ret;
}

double TabuaMDTCpp::qx(std::vector<int> x, double t) const {
	double ret = 0.0;
	for (int i = 0; i < m_numero_decrementos; i++)
	{
		ret += qx_j(x, t, i);
	}
	return ret;
}

double TabuaMDTCpp::tpx(std::vector<int> x, double t) const {
	if (x.size() != m_numero_decrementos) {
		throw std::invalid_argument("x deve ser um vetor com tamanho igual ao numero de decrementos.");
	}
	double ret = 1.0;
	for (size_t i = 0; i < m_numero_decrementos; i++)
	{
		ret = ret * m_tabuas[i].tpx(x[i], t);
	}
	return ret;
}

std::vector<double> TabuaMDTCpp::qx(std::vector<int> x, std::vector<double> t) const {
	std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = qx(x, t[i]);
    }
    return ret;
}

std::vector<double> TabuaMDTCpp::tpx(std::vector<int> x, std::vector<double> t) const {
	std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = tpx(x, t[i]);
    }
    return ret;
}

double TabuaMDTCpp::tempo_futuro_maximo(std::vector<int> x) const {
	if (x.size() != m_numero_decrementos) {
		throw std::invalid_argument("x deve ser um vetor com tamanho igual ao numero de decrementos.");
	}
	std::vector<double> ret(m_numero_decrementos);
	for (size_t i = 0; i < m_numero_decrementos; i++)
	{
		ret[i] = m_tabuas[i].tempo_futuro_maximo(x[i]);
	}
	return *std::min_element(ret.begin(), ret.end());
}

