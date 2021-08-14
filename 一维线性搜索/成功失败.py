import matplotlib.pyplot as plt
import numpy as np
from 求导 import first_derivative, second_derivative
from Functions import fun2
    
def fun(x):
    return x**3 - 2*x + 1

def display(fun, x0=6, a=-1, b=6, h=6, delta=0.001):
    # fun: 输入的函数, 二维
    # x0: 初始点坐标
    # a: 范围的下限
    # b: 范围的上限
    # delta: 步长
    # return: 迭代的次数，结果的坐标
    
    ax=plt.gca()
    X = np.linspace(a, b, 100)
    plt.plot(X, fun(X), color='y')

    # h = np.random.randint(1, 10)
    x = x0
    times = 0
    while abs(h) > delta:
        ax.scatter(x,fun(x), c='green',marker='o')
        plt.pause(0.2)
        times += 1
        if fun(x + h) < fun(x):
            h *= 2
            x += h
        else:
            h *= -1 / 4
            x += h
        
    ax.scatter(x,fun(x), c='red',marker='o')
    plt.show()
    return times, x

if __name__ == "__main__":
    times, x = display(fun, x0=-0.5, h=0.5)
    print("迭代次数为:{:}, 极小值点为:{:}".format(times, x))
