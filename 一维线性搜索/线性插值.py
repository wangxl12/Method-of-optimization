import matplotlib.pyplot as plt
import numpy as np
from Functions import fun1


def insertValue(fun, x1, x2, x3):
    # print(x1, x2, x3)
    c1 = (fun(x1) - fun(x3)) / (x1 - x3)
    c2 = ((fun(x1) - fun(x2)) / (x1 - x2) - c1) / (x2 - x3)
    return (x1 + x3 - c1 / c2) / 2


def display(fun, x0=6, a=-1, b=6, delta=0.001):
    ax = plt.gca()
    X = np.linspace(a, b, 100)
    plt.plot(X, fun(X), color='y')

    # h = np.random.randint(1, 10)
    h = 6  # 步长
    x = x0
    x1 = None
    x3 = None
    # 通过成功失败方法确定初始区间
    while True:
        ax.scatter(x, fun(x), c='green', marker='o')
        if fun(x + h) < fun(x):
            h *= 2
            x += h
        else:
            if h > 0:
                x3 = x + h
            else:
                x1 = x + h
            h *= -1 / 4
            x += h
        if x3 is not None and x1 is not None:
            break
        plt.pause(0.2)
    # 将左右区间展示出来
    plt.plot([x1] * 500, list(range(-250, 250)), color='blue')
    plt.pause(0.2)
    plt.plot([x3] * 500, list(range(-250, 250)), color='blue')
    plt.pause(0.2)

    # 插值算法开始：
    x2 = (x1 + x3) / 2
    x0 = insertValue(fun, x1, x2, x3)
    times = 0
    while abs(x2 - x0) >= delta:
        times += 1
        if fun(x0) < fun(x2) and x0 <= x2:
            x3 = x2
        elif fun(x0) < fun(x2) and x0 > x2:
            x1 = x2
        x2 = x0
        x0 = insertValue(fun, x1, x2, x3)
        ax.scatter(x0, fun(x0), c='green', marker='o')
        plt.pause(0.2)
    ax.scatter(x0, fun(x0), c='red', marker='o')
    plt.show()
    return times, x0


if __name__ == "__main__":
    times, x = display(fun1)
    print("迭代次数为:{:}, 极小值点为:{:}".format(times, x))
