from matplotlib import pyplot as plt
import numpy as np
from tools import FirstDerivative, SecondDerivative, GetA, GetInverseMatrix
from functions import fun2, fun1, fun3, fun4, fun5, fun6, fun7, fun8


def fun(x1, x2):
    return 4*(x1-5)**2 + (x2-6)**2
    
def display(x_range, y_range, function, X0=None, delta=0.01):
    if X0 is None:
        X0 = [5, 5]
    gradients = None
    if len(X0) == 2:
        gradients = np.eye(2)
    elif len(X0) == 3:
        gradients = np.eye(3)
    fig = plt.figure(figsize=(7, 7))  # 定义新的三维坐标轴
    ax3 = plt.axes(projection='3d')

    # 定义三维数据
    xx = np.arange(x_range[0], x_range[1], 0.5)
    yy = np.arange(y_range[0], y_range[1], 0.5)
    X, Y = np.meshgrid(xx, yy)
    Z = function(X, Y)

    ax3.contour(X, Y, Z, 20, offset=-2, cmap='rainbow')  # 等高线图，要设置offset，为Z的最小值
    ax3.plot_wireframe(X, Y, Z, color='gray')

    X = np.array([[X0[0]], [X0[1]]])
    X_new = np.array([[float('inf')], [float('inf')]])

    count = 0
    grad_flag = 0  # 用来标志轮换的方向
    grad_list = []
    fx = []

    while abs((X[0, 0] - X_new[0, 0]) ** 2 + (X[1, 0] - X_new[1, 0]) ** 2) > delta:
        if count != 0:  # count=0的时候new还没有更新，不能将其值赋给X
            X = X_new
        fx.append(function(X[0, 0], X[1, 0]))
        grad = gradients[grad_flag].reshape(-1, 1)  # 获取下降的方向
        grad_list.append(grad)

        ax3.scatter3D(X[0, 0], X[1, 0], function(X[0, 0], X[1, 0]), c='g', s=50)

        a = GetA(function, X, -grad, coordinate_rotation=True)  # 计算步长,传进去的一定是方向，即负梯度
        if a is None:
            print("无非负实数步长值！请修改X0的初始值")
            return
        elif abs(a) < 0.01:  # 步长太小认为更新的不多，直接结束
            print("步长过小，下降效果将不明显，认为已找到了最优解")
            break

        X_new = np.array(X) - a * grad  # a是下降的步长

        count += 1
        grad_flag += 1
        if grad_flag > len(gradients) - 1:
            grad_flag = 0
        plt.pause(0.4)

    ax3.scatter3D(X_new[0, 0], X_new[1, 0], function(X_new[0, 0], X_new[1, 0]), c='r', label='最优点', s=50)

    if X_new[0] == float('inf') and X_new[1] == float('inf'):
        X_new = X
    # print(type(X_new[0, 0]), type(X_new[1, 0]), type(function(X_new[0, 0], X_new[1, 0])))

    if count == 0:
        count += 1
    print("一共迭代了{:}次\n极小值点为({:.2f},{:.2f})\n极小值为{:.2f}"
          .format(count, float(X_new[0, 0]), float(X_new[1, 0]), float(function(X_new[0, 0], X_new[1, 0]))))
    # print(grad_list)
    # print("fx = ", fx)

    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_zlabel('z')
    ax3.set_title('3D contour')
    plt.show()


if __name__ == "__main__":
    display((-5, 8), (-3, 10), fun, X0=[-5, 4])  # fun4
