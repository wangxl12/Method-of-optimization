from matplotlib import pyplot as plt
import numpy as np
from tools import FirstDerivative, SecondDerivative, GetA, GetInverseMatrix
from functions import fun2, fun1, fun3, fun4, fun5, fun6, fun7, fun8

def fun(x1, x2):
    return x1**2 + 25*x2**2

def display(x_range, y_range, function, a=1, X0=None, delta=0.01):
    if X0 is None:
        X0 = [5, 5]

    fig = plt.figure(figsize=(7, 7))  # 定义新的三维坐标轴
    ax3 = plt.axes(projection='3d')

    # 定义三维数据
    xx = np.arange(x_range[0], x_range[1], 0.5)
    yy = np.arange(y_range[0], y_range[1], 0.5)
    X, Y = np.meshgrid(xx, yy)
    Z = function(X, Y)

    ax3.contour(X, Y, Z, 20, zdim='z', offset=-2, cmap='rainbow')  # 等高线图，要设置offset，为Z的最小值
    ax3.plot_wireframe(X, Y, Z, color='gray')

    X = np.array([[X0[0]], [X0[1]]])
    X_new = np.array([[float('inf')], [float('inf')]])

    count = 0
    grad_list = []
    fx = []

    while abs((X[0, 0] - X_new[0, 0]) ** 2 + (X[1, 0] - X_new[1, 0]) ** 2) > delta:
        if count != 0:  # count=0的时候new还没有更新，不能将其值赋给X
            X = X_new

        fx.append(function(X[0, 0], X[1, 0]))
        grad = np.array(FirstDerivative(X[0, 0], X[1, 0], function)).reshape(2, 1)  # 计算梯度
        grad_list.append(grad)

        # ！！！！！！！！！！！！！如果此时梯度为零，说明此时点为驻点！！！！！！！！！！！！！！！
        if abs(grad[0, 0]) < 0.001 and abs(grad[1, 0]) < 0.001:
            # 如果给一个微小的扰动大于此时的值，那么认为此时为极小值点
            if function(X[0, 0] + delta, X[1, 0] + delta) > function(X[0, 0], X[1, 0]):
                print("最优点")
                ax3.scatter3D(X[0, 0], X[1, 0], function(X[0, 0], X[1, 0]), c='y', label='最优点', s=50)
                break

        ax3.scatter3D(X[0, 0], X[1, 0], function(X[0, 0], X[1, 0]), c='g', s=50)

        second_derivative = SecondDerivative(X[0, 0], X[1, 0], function)  # 求二阶导
        inverse_matrix = GetInverseMatrix(second_derivative)  # 求二阶导矩阵的逆

        X_new = np.array(X) - a * np.matmul(inverse_matrix, grad)  # a是下降的步长

        count += 1

        plt.pause(0.4)

    ax3.scatter3D(X_new[0, 0], X_new[1, 0], function(X_new[0, 0], X_new[1, 0]), c='r', label='最优点', s=50)

    if X_new[0] == float('inf') and X_new[1] == float('inf'):
        X_new = X

    if count == 0:
        count += 1
    print("一共迭代了{:}次\n极小值点为({:.2f},{:.2f})\n极小值为{:.2f}"
          .format(count, float(X_new[0, 0]), float(X_new[1, 0]), float(function(X_new[0, 0], X_new[1, 0]))))
    print(grad_list)
    print("fx = ", fx)

    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_zlabel('z')
    ax3.set_title('3D contour')
    plt.show()


if __name__ == "__main__":
    display((-5, 10), (-5, 7), fun, X0=[2, 2])
