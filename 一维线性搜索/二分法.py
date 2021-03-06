import matplotlib.pyplot as plt
import numpy as np
from 求导 import first_derivative, second_derivative
from Functions import fun1


def display(fun, x0=6, a=-1, b=6, delta=0.001):
    X = np.linspace(a, b, 100)
    plt.plot(X, fun(X), color='y')

    times = 0
    pre_a = a
    pre_b = b
    while abs(b - a) >= delta:
        times += 1
        plt.plot([a] * 20, list(range(-10, 10)), color='red')
        plt.plot([b] * 20, list(range(-10, 10)), color='red')
        x = (a + b) / 2
        if first_derivative(fun, x) < 0:
            a = x
        elif first_derivative(fun, x) > 0:
            b = x
        else:
            break
        plt.pause(0.4)
        plt.plot([pre_a] * 20, list(range(-10, 10)), color='green')
        plt.plot([pre_b] * 20, list(range(-10, 10)), color='green')
        pre_a = a
        pre_b = b
    plt.plot([x] * 500, list(range(-250, 250)), color='red')
    plt.plot([x] * 500, list(range(-250, 250)), color='red')
    plt.show()
    return times, x

if __name__ == "__main__":
    times, x = display(fun1)
    print("迭代次数为:{:}, 极小值点为:{:}".format(times, x))