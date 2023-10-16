# tabatu
Definição de tábuas atuariais em python com códigos em C++ para melhor performance.

## Instalação

O pacote pode ser instalado diretamente do PyPI:

```
pip install tabatu
```

## Uso

O pacote fornece 3 classes para lidar com tábuas atuariais: `Tabua`, `TabuaMDT`e `TabuaMultiplasVidas`.

Uma tábua pode ser criada diretamente a partir de um array de taxas.

```
>>> from tabatu import Tabua
>>> qx = [0.1, 0.2, 0.3, 0.4, 0.5, 1.0]
>>> tabua = Tabua(qx)
>>> tabua.tpx([2], [1,2,3])
array([0.7 , 0.42, 0.21])
tabua.t_qx([2], [1,2,3])
array([0.28, 0.21, 0.21])
```

A tábua fornece métodos para cálculo de probabilidades de sobrevivência e morte, além de fornecer algumas utilidades 
como tempo de vida futuro máximo e um indicador a respeito do fechamento da tábua ser platô ou não.

## Documentação

A documentação está disponível [aqui](https://vitorcapdeville.github.io/tabuas-atuariais/).
