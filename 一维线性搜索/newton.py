import numpy as np
import matplotlib.pyplot as plt
from 求导 import first_derivative, second_derivative
from Functions import fun1


def display(fun, x0=6, a=-1, b=6, delta=0.001):
    ax = plt.gca()
    X = np.linspace(a, b, 100)
    plt.plot(X, fun(X), color='y')

    x = x0
    times = 0
    while abs(first_derivative(fun, x)) >= delta:
        times += 1
        x -= first_derivative(fun, x) / second_derivative(fun, x)
        ax.scatter(x, fun(x), c='green', marker='o')
        plt.pause(0.2)
    ax.scatter(x, fun(x), c='red', marker='o')
    plt.show()
    return times, x


if __name__ == "__main__":
    times, x = display(fun1)
    print("迭代次数为:{:}, 极小值点为:{:}".format(times, x))
