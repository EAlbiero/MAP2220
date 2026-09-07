"""
Autores:

Enzo Albiero Mattos - 12557060

"""

###########################################
"""
Ideia: pensei em fazer cada item (3.1, 3.2 e 4) como uma função própria, depois
vamos chamando tudo dentro da main para rodar as simulações que precisarmos.

"""
###########################################

import numpy as np
import matplotlib.pyplot as plt

# Defini esses números só para testar o funcionamento do código, depois
# podemos colocar valores melhores para o relatório
ATOL = 1e-6
RTOL = 1e-6
MAXIT = 100

def main():
    return


def quedaCorpo(t0: float, t1: float, v0: float, v1: float, m: float, g: float):
    f = lambda k: (-np.exp(-t1*k/m) + np.exp(-t0*k/m))(m*g - v0*k)/(k*(v1 - v0))

    return


def alturaFios():
    return


def quadratura():
    return


def encontraRaiz(a: float, b: float, x0: float, f: function, df: function) -> float:
    acabou = False
    iteracao = 0
    x1 = x0
    while (not acabou):
        if deveUsarMetodoDeNewton(a, b, x0, x1, f, df):
            x1 = newton(x0, f, df)
            # Atualiza o intervalo [a,b]
            if x1<x0:
                b = x1
            else:
                a = x1
        else:
            a, b, x1 = dicotomia(a, b, f)

        iteracao += 1
        acabou = devePararExecucao(x0, x1, f, iteracao)
        x0 = x1

    return x1


def newton(x0: float, f: function, df: function) -> float:
    return x0 - (f(x0)/df)(x0)


def dicotomia(a: float, b: float, f: function) -> tuple[float, float]:
    m = (a+b)/2
    fm = f(m)
    fa = f(a)
    fb = f(b)

    if fa*fm < 0:
        b = m
    else:
        a = m
    # m vai ser o nosso próximo valor por xm
    # (a, b) é retornado com redundância para facilitar o uso do
    # intervalo em outras funções
    return a, b, m


def devePararExecucao(x0: float, x1: float, f: function, iteracao: int) -> bool:
    global ATOL
    global RTOL

    if abs(x1-x0) < ATOL + RTOL*(abs(x1)):
        print(f"Tolerância atingida")
        return True
    if iteracao == MAXIT:
        print(f"Número máximo de iterações atingido: {MAXIT}")
        return True
    if f(x1) == 0:
        print("Raíz exata encontrada")
        return True

    return False


def deveUsarMetodoDeNewton(a: float, b: float, x0: float, x1: float, f: function, df: function) -> float:
    return ( (x1-a)*df(x1) - f(x1) )*( (x1-b)*df(x1) - f(x1) ) < 0 and 2*abs(f(x1)) < abs(df(x1)*(x1-x0))

main()