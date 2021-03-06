import numpy as np
import matplotlib.pyplot as plt
from Functions import fun1


def display(fun, x0=6, a=-1, b=6, delta=0.001):
    X = np.linspace(a, b, 100)
    plt.plot(X, fun(X), color='y')

    x = x0
    times = 0
    t = (np.sqrt(5) - 1) / 2 
    pre_a = a
    pre_b = b
    while abs(b - a) > delta:
        plt.plot([a] * 20, list(range(-10, 10)), color='red')
        plt.plot([b] * 20, list(range(-10, 10)), color='red')
        
        times += 1
        x1 = a + (1 - t) * (b - a)
        x2 = a + t * (b - a)
        if fun(x1) - fun(x2) > 0:
            a = x1
            x1 = x2
            x2 = a + t * (b - a)
        else:
            b = x2
            x2 = x1
            x1 = a + (1 - t) * (b - a)
        # ax.scatter(x,fun(x), c='green',marker='o')
        plt.pause(0.4)
        plt.plot([pre_a] * 20, list(range(-10, 10)), color='green')
        plt.plot([pre_b] * 20, list(range(-10, 10)), color='green')
        pre_a = a
        pre_b = b
    x = (a + b) / 2
    # ax.scatter(x,fun(x), c='red',marker='o')
    plt.plot([x] * 500, list(range(-250, 250)), color='red')
    plt.plot([x] * 500, list(range(-250, 250)), color='red')
    plt.show()
    return times, x

if __name__ == "__main__":
    times, x = display(fun1)
    print("迭代次数为:{:}, 极小值点为:{:}".format(times, x))
