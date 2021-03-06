from matplotlib import pyplot as plt
import numpy as np
from tools import FirstDerivative, SecondDerivative, GetA, GetInverseMatrix, GetMagnitude
from functions import fun2, fun1, fun3, fun4, fun5, fun6, fun7, fun8


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

    ax3.contour(X, Y, Z, 20, offset=-2, cmap='rainbow')  # 等高线图，要设置offset，为Z的最小值
    ax3.plot_wireframe(X, Y, Z, color='gray')

    X = np.array([[X0[0]], [X0[1]]])
    X_new = np.array([[float('inf')], [float('inf')]])

    count = 0
    beta = None
    pre_magnitude = float('inf')  # k + 1
    cur_magnitude = float('inf')  # k
    grad = None
    pre_grad = None  # k + 1
    cur_grad = None  # k
    direction = None  # the direction
    grad_list = []
    fx = []

    # while abs((X[0, 0] - X_new[0, 0]) ** 2 + (X[1, 0] - X_new[1, 0]) ** 2) > delta:
    while pre_magnitude > delta:

        if count != 0:  # count=0的时候new还没有更新，不能将其值赋给X
            cur_grad = FirstDerivative(X[0], X[1], function).reshape(-1, 1)
            cur_magnitude = GetMagnitude(cur_grad)
            beta = cur_magnitude / pre_magnitude
            direction = -cur_grad + beta * (-pre_grad)
        else:
            cur_grad = FirstDerivative(X[0], X[1], function).reshape(-1, 1)
            direction = -cur_grad  # 第一次方向直接取的是负梯度方向
        fx.append(function(X[0, 0], X[1, 0]))
        grad_list.append(cur_grad)

        ax3.scatter3D(X[0, 0], X[1, 0], function(X[0, 0], X[1, 0]), c='g', s=50)
        # print(X.reshape(-1, ), '\t', direction.reshape(-1, ))

        if cur_magnitude < delta:  # 如果当前梯度的模为0，说明找到了最优点，需要在计算a之前退出，不然会报错
            print("最优点")
            break

        a = GetA(function, X, direction)  # 计算步长,只能传入梯度，不能是方向，因为函数本身会取负梯度
        if a is None:
            print("无非负实数步长值！请修改X0的初始值")
            return
        elif abs(a) < 0.01:  # 步长太小认为更新的不多，直接结束
            print("步长过小，下降效果将不明显，认为已找到了最优解")
            break

        # print(a)
        X_new = np.array(X) + a * direction  # a是下降的步长

        pre_grad = cur_grad
        pre_magnitude = GetMagnitude(pre_grad)  # 计算向量的模
        X = X_new
        count += 1
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
    display((-5, 6), (-5, 7), fun7, X0=[-5, 4])  # fun4, fun5
