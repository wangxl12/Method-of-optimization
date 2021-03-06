from matplotlib import pyplot as plt
import numpy as np
from tools import FirstDerivative, SecondDerivative, GetA, GetInverseMatrix, GetTransposeMatrix
from functions import fun2, fun1, fun3, fun4, fun5, fun6, fun7, fun8


def GetStructureMatrix(delta_grad, delta_x, A):
    """
    get the structure matrix
    :param delta_grad:
    :param delta_x:
    :param A:
    :return: get A
    """
    delta_A = np.matmul(delta_x, GetTransposeMatrix(delta_x)) / \
              np.matmul(GetTransposeMatrix(delta_x), delta_grad) - \
              np.matmul(np.matmul(np.matmul(A, delta_grad), GetTransposeMatrix(delta_grad)), A) / \
              np.matmul(np.matmul(GetTransposeMatrix(delta_grad), A), delta_grad)
    return delta_A


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
    cur_direction = None
    pre_grad = None
    cur_grad = None
    grad_list = []
    fx = []
    A = None  # 构造矩阵

    while abs((X[0, 0] - X_new[0, 0]) ** 2 + (X[1, 0] - X_new[1, 0]) ** 2) > delta:
        if count != 0:  # count=0的时候new还没有更新，不能将其值赋给X
            delta_x = X_new - X  # 计算X的改变量
            X = X_new
            pre_grad = cur_grad
            cur_grad = np.array(FirstDerivative(X[0, 0], X[1, 0], function)).reshape(2, 1)  # 计算梯度

            delta_grad = cur_grad - pre_grad  # 计算梯度的改变量
            # print(cur_grad, "\n", pre_grad)
            delta_A = GetStructureMatrix(delta_grad, delta_x, A)  # 计算构造矩阵的变量
            # print(type(A))
            try:
                A = delta_A + A  # 更新构造矩阵
            except:
                print("计算A的时候出错！")
                return

        else:
            cur_grad = np.array(FirstDerivative(X[0, 0], X[1, 0], function)).reshape(2, 1)  # 计算梯度
            A = np.eye(2)  # 默认是二维,第一次迭代的构造矩阵是单位矩阵

        fx.append(function(X[0, 0], X[1, 0]))
        grad_list.append(cur_grad)

        cur_direction = np.matmul(A, -cur_grad)  # 计算当前的下降方向
        # print(cur_direction)

        # ！！！！！！！！！！！！！如果此时梯度为零，说明此时点为驻点！！！！！！！！！！！！！！！
        if abs(cur_direction[0, 0]) < 0.001 and abs(cur_direction[1, 0]) < 0.001:
            # 如果给一个微小的扰动大于此时的值，那么认为此时为极小值点
            if function(X[0, 0] + delta, X[1, 0] + delta) > function(X[0, 0], X[1, 0]):
                print("最优点")
                ax3.scatter3D(X[0, 0], X[1, 0], function(X[0, 0], X[1, 0]), c='y', label='最优点', s=50)
                break

        ax3.scatter3D(X[0, 0], X[1, 0], function(X[0, 0], X[1, 0]), c='g', s=50)
        a = GetA(function, X, cur_direction)  # 计算步长，传进去的一定是方向，即负梯度
        # print(a)
        if a is None:
            print("无非负实数步长值！请修改X0的初始值")
            return
        elif abs(a) < 0.01:  # 步长太小认为更新的不多，直接结束
            print("a = ", a)
            print("步长过小，下降效果将不明显，认为已找到了最优解")
            break

        X_new = np.array(X) + a * cur_direction  # a是下降的步长

        count += 1
        plt.pause(0.4)

    ax3.scatter3D(X_new[0, 0], X_new[1, 0], function(X_new[0, 0], X_new[1, 0]), c='r', label='最优点', s=50)

    if X_new[0] == float('inf') and X_new[1] == float('inf'):
        X_new = X

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
    display((-5, 10), (-5, 7), fun1, X0=[-5, 4])  # fun5,fun4
