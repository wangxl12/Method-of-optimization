from matplotlib import pyplot as plt
import numpy as np
from tools import FirstDerivative, SecondDerivative, GetA, GetInverseMatrix
from functions import fun2, fun1, fun3, fun4, fun5, fun6, fun7, fun8
import sympy as sy


def display(x_range, y_range, function, X0=None, delta=0.01):
    if X0 is None:
        X0 = [5, 5]
    fig = plt.figure(figsize=(7, 7))  # 定义新的三维坐标轴
    ax3 = plt.axes(projection='3d')

    # 定义三维数据
    xx = np.arange(x_range[0], x_range[1], 0.5)
    yy = np.arange(y_range[0], y_range[1], 0.5)
    X, Y = np.meshgrid(xx, yy)
    Z = function(X, Y)

    # ax3.plot_surface(X, Y, Z, cmap='binary')
    # ax3.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='binary')  # 其中row和cloum_stride为横竖方向的绘图采样步长，越小越精细
    # ax3.contour(X, Y, Z, zdim='z', offset=-2, cmap='rainbow')  # 等高线图，要设置offset，为Z的最小值
    ax3.contour(X, Y, Z, offset=-2, cmap='rainbow')  # 等高线图，要设置offset，为Z的最小值
    # ax3.contour3D(X, Y, Z, 50, cmap='rainbow')  # 等高线图，要设置offset，为Z的最小值
    ax3.plot_wireframe(X, Y, Z, color='gray')

    X = np.array(X0)
    X_new = np.array([float('inf'), float('inf')])

    count = 0
    a_list = []
    grad_list = []

    while abs((X[0] - X_new[0]) ** 2 + (X[1] - X_new[1]) ** 2) > delta:
        if count != 0:  # count=0的时候new还没有更新，不能将其值赋给X
            X = X_new

        grad = np.array(FirstDerivative(X[0], X[1], function))  # 计算梯度

        grad_list.append(grad)

        # ！！！！！！！！！！！！！如果此时梯度为零，说明此时点为驻点！！！！！！！！！！！！！！！
        if abs(grad[0]) < 0.001 and abs(grad[1]) < 0.001:
            # 如果给一个微小的扰动大于此时的值，那么认为此时为极小值点
            if function(X[0] + delta, X[1] + delta) > function(X[0], X[1]):
                print("最优点")

                ax3.scatter3D(X[0], X[1], function(X[0], X[1]), c='y', label='最优点', s=50)
                break

        ax3.scatter3D(X[0], X[1], function(X[0], X[1]), c='g', s=50)

        a = GetA(function, X, -grad)  # 核心下降公式，传进去的一定是方向，即负梯度
        if a is None:
            print("无非负实数步长值！请修改X0的初始值")
            return
        elif abs(a) < 0.01:  # 步长太小认为更新的不多，直接结束
            print("步长过小，下降效果将不明显，认为已找到了最优解")
            break
        a_list.append(a)

        X_new = np.array(X) - a * grad  # a是下降的步长

        count += 1
        # print("x_new = {:}, x = {:}".format(X_new, X))
        plt.pause(0.4)

    if X_new[0] == float('inf') and X_new[1] == float('inf'):
        X_new = X

    ax3.scatter3D(X_new[0], X_new[1], function(X_new[0], X_new[1]), c='r', label='最优点', s=50)

    if count == 0:
        count += 1
    print("一共迭代了{:}次\n极小值点为({:.2f},{:.2f})\n极小值为{:.2f}"
          .format(count, float(X_new[0]), float(X_new[1]), float(function(X_new[0], X_new[1]))))
    # print(a_list)
    # print(grad_list)
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_zlabel('z')
    ax3.set_title('3D contour')
    plt.show()


if __name__ == "__main__":
    display((-5, 10), (-5, 7), fun3, X0=[-5, 4])  # fun4, fun5
# import tkinter as tk
#
# window = tk.Tk()
# window.title('my window')
# window.geometry('300x100')
#
# # 这里是窗口的内容
# m = """
# function = x^20 + 2*x + 20
# # ministep = 20
# """
#
# l = tk.Label(window,
#              text=m,  # 标签的文字
#              bg='green',  # 背景颜色
#              font=('Arial', 12),  # 字体和字体大小
#              width=30, height=30)  # 标签长宽
# l.pack()  # 固定窗口位置
# window.mainloop()
