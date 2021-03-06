import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import *  # 引进用于调用“变量控制滚动条”的包
from mpl_toolkits import mplot3d  # 用于绘制3D图形


# 梯度函数的导数
def gradJ1(x, y):
    return x / (np.sqrt(x ** 2 + y ** 2)) * np.cos(np.sqrt(x ** 2 + y ** 2))


def gradJ2(x, y):
    return y / (np.sqrt(x ** 2 + y ** 2)) * np.cos(np.sqrt(x ** 2 + y ** 2))


# 梯度函数
def f(X, Y):
    # return np.sin(np.sqrt(x ** 2 + y ** 2))
    Z = X ** 2 + 2 * Y ** 2 - 2 * X * Y - 4 * X
    return Z


def train(lr, epoch, theta1, theta2, up, dirc):
    # 下面的三个数组，由于记录迭代过程的路径
    t1 = [theta1]
    t2 = [theta2]
    z = [f(theta1, theta2)]
    for i in range(epoch):
        gradient = gradJ1(theta1, theta2)
        theta1 = theta1 - lr * gradient
        t1.append(theta1)
        gradient = gradJ2(theta1, theta2)
        theta2 = theta2 - lr * gradient
        t2.append(theta2)
        z.append(f(theta1, theta2))

    plt.figure(figsize=(12, 12))  # 设置画布大小
    x = np.linspace(-6, 6, 100)
    y = np.linspace(-6, 6, 100)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    ax = plt.axes(projection='3d')
    ax.contour3D(X, Y, Z, 50, cmap='binary')  # 等高线图
    # ax.plot_surface(X, Y, Z, cmap='binary')

    ax.scatter3D(t1, t2, z, c='r', marker='o')  # 散点图
    # 调整观察角度和方位角。这里将俯仰角设为45度，把方位角调整为45度
    ax.view_init(up, dirc)
    plt.show()


# 可以随时调节，查看效果 (最小值，最大值，步长) 具体关于ipywidgets包详细怎么用可自行搜索，若只是想简单使用，模仿下面的方式使用即可
@interact(lr=(0, 2, 0.01), epoch=(1, 100, 1), init_theta1=(-6, 6, 0.1), init_theta2=(-6, 6, 0.1), up=(-180, 180, 1),
          dirc=(-180, 180, 1), continuous_update=False)
# lr为学习率（步长） epoch为迭代次数   init_theta为初始参数的设置 up,dirc用于控制视角
def visualize_gradient_descent(lr=0.2, epoch=20, init_theta1=2, init_theta2=0, up=45, dirc=45):
    train(lr, epoch, init_theta1, init_theta2, up, dirc)

visualize_gradient_descent()