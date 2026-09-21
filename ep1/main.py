"""
Autores:

Juliana Mika Suzukawa - 15643026 
Enzo Albiero Mattos - 12557060

"""

###########################################

import numpy as np
import matplotlib.pyplot as plt
import sys

plt.style.use('ggplot')

ATOL = 1e-10
RTOL = 1e-10
MAXIT = 200

# Passo utilizado para gerar os gráficos dos problemas
dx = 0.001

def main():
    ex = float(sys.argv[1])
    a = float(sys.argv[2])
    b = float(sys.argv[3])

    if ex == Exercicio.QUEDA:
        quedaCorpo(a=a, b=b, t0=0, t1=2, v0=3, v1=20, m=1, g=10)
    elif ex == Exercicio.FIOS:
        alturaFios(a=a, b=b, h=10, dy=0.5)
    elif ex == Exercicio.QUADRATURA:
        quadratura()


def quedaCorpo(a: float, b:float, t0: float, t1: float, v0: float, v1: float, m: float, g: float):
    f = lambda k: (-np.exp(-t1*k/m) + np.exp(-t0*k/m)) * (m*g - v0*k) - (k*(v1 - v0))
    termo_exp = lambda t, k: (t*g + v0 - (t*v0*k/m))*np.exp(-t*k/m)
    df = lambda k: (termo_exp(t1, k) - termo_exp(t0, k)) + v0 - v1

    # Plot de f(k) para estimarmos o intervalo a ser utilizado
    x = np.arange(a, b, dx)
    y = f(x)
    plt.xlabel('$k$')
    plt.ylabel('$f(k)$')
    plt.title('Esboço de $y=f(k)$')
    plt.plot(x, y)
    plt.savefig("plot_3_1.png")

    k_aproximado = encontraRaiz(a, b, f, df)
    print(f"Valor aproximado: k={k_aproximado}")

    # Testes de sanidade: conferindo os valores de v(t)
    # em t=0 e t=2
    vt = lambda t: (m*g - (m*g - v0*k_aproximado)*np.exp(-k_aproximado*t/m))/k_aproximado
    print(f"Velocidades calculadas com o valor de k encontrado:")
    print(f"v(0) = {vt(0)}, erro {abs(3-vt(0))}")
    print(f"v(2) = {vt(2)}, erro {abs(20-vt(2))}")
    return

def alturaFios(a: float, b:float, h: float, dy: float, ):
    f = lambda beta: beta*(np.cosh(h/beta) - np.cosh(0)) - dy
    df = lambda beta: np.cosh(h/beta) - h*np.cosh(h/beta)/beta - 1

    # Plot de f(beta)
    x = np.arange(a, b, dx)
    y = f(x)
    plt.xlabel('$\\beta$')
    plt.ylabel('$f(\\beta)$')
    plt.title('Esboço de $f(\\beta)$')
    plt.plot(x, y)
    plt.savefig("plot_3_2.png")

    beta_aproximado = encontraRaiz(a, b, f, df)
    print(f"Valor aproximado: beta={beta_aproximado}")

    # Teste de sanidade
    dh = lambda beta, x1, x2: beta*(np.cosh(x2/beta) - np.cosh(x1/beta))
    dy_aproximado = dh(beta_aproximado, 0, h)
    print(f"Diferença de altura entre x=0 e x=10: {dy_aproximado}")
    print(f"Erro comparado com o valor esperado: {abs(0.5-dy_aproximado)}")
    return

def quadratura():
    return

def encontraRaiz(a: float, b: float, f: function, df: function) -> float:
    acabou = False
    iteracao = 0
    x0 = extremoMaisProximo(a, b, f)
    x1 = x0
    while (not acabou):
        if deveUsarMetodoDeNewton(a, b, x0, x1, f, df):
            x0 = x1
            x1 = newton(x0, f, df)
            # Atualiza o intervalo [a,b] de acordo com onde
            # f troca de sinal
            if np.sign(f(a)) != np.sign(f(x1)):
                b = x1
            else:
                a = x1
        else:
            x0 = x1
            a, b, x1 = dicotomia(a, b, f)

        iteracao += 1
        acabou = devePararExecucao(x0, x1, f, iteracao)

    print(f"Número de iterações realizadas: {iteracao}")
    return x1

def newton(x0: float, f: function, df: function) -> float:
    return x0 - (f(x0)/df(x0))

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
        print(f"Valor aproximado da raiz após {MAXIT} iterações: {x1}")
        return True
    if f(x1) == 0:
        print("Raíz exata encontrada")
        return True

    return False

def deveUsarMetodoDeNewton(a: float, b: float, x0: float, x1: float, f: function, df: function) -> float:
    return ( (x1-a)*df(x1) - f(x1) )*( (x1-b)*df(x1) - f(x1) ) < 0 and 2*abs(f(x1)) < abs(df(x1)*(x1-x0))

def extremoMaisProximo(a: float, b: float, f: function) -> float:
    if np.sign(f(a)) == np.sign(f((b-a)/2)):
        return b
    return a

class Exercicio():
    QUEDA = 1
    FIOS = 2
    QUADRATURA = 3

main()