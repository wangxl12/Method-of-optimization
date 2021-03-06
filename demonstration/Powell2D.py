from matplotlib import pyplot as plt
import numpy as np
from tools import FirstDerivative, SecondDerivative, GetA, GetInverseMatrix, GetTransposeMatrix
from functions import fun2, fun1, fun3, fun4, fun5, fun6, fun7, fun8


def judge_a(a):
    if a is None:
        print("无非负实数步长值！请修改X0的初始值")
        return 1
    elif abs(a) < 0.01:  # 步长太小认为更新的不多，直接结束
        print("步长过小，下降效果将不明显，认为已找到了最优解")
        return 2
    else:
        return 0


def display(x_range, y_range, function, bottom=0, scatter_size=30, X0=None, delta=0.01):
    if X0 is None:
        X0 = [5, 5]
    fig = plt.figure(figsize=(8, 8))  # 定义新的三维坐标轴
    ax3 = plt.axes(projection='3d')
    ax3.view_init(elev=90, azim=90)
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_zlabel('z')
    ax3.set_title('3D contour')

    # 定义三维数据
    xx = np.arange(x_range[0], x_range[1], 0.5)
    yy = np.arange(y_range[0], y_range[1], 0.5)
    X, Y = np.meshgrid(xx, yy)
    Z = function(X, Y)

    ax3.contour(X, Y, Z, 20, offset=bottom, cmap='rainbow')  # 等高线图，要设置offset，为Z的最小值
    # ax3.plot_wireframe(X, Y, Z, color='gray')

    count = 0
    direction1 = np.array([1, 0]).reshape(2, 1)
    direction2 = np.array([0, 1]).reshape(2, 1)
    x1 = np.array([[X0[0]], [X0[1]]])
    x3 = np.array([[float('inf')], [float('inf')]])
    good_results = []
    final_point = None

    while abs((x1[0, 0] - x3[0, 0]) ** 2 + (x1[1, 0] - x3[1, 0]) ** 2) > delta:
        plt.pause(0.01)
        yield ''

        if count != 0:
            ax3.scatter3D(x3[0, 0], x3[1, 0], bottom, c='g', s=scatter_size)
        ax3.scatter3D(x1[0, 0], x1[1, 0], bottom, c='b', s=scatter_size)
        ax3.text(x1[0, 0], x1[1, 0], bottom, str((count + 1, 1)))
        plt.pause(0.01)
        yield str('x1 = ') + str((round(x1[0, 0], 2), round(x1[1, 0], 2)))

        if count == 0:  # count=0的时候new还没有更新，不能将其值赋给X
            direction1 = -np.eye(2)[0].reshape(-1, 1)
            direction2 = -np.eye(2)[1].reshape(-1, 1)

        a = GetA(function, x1, direction1)  # 计算步长，传进去的一定是方向，即负梯度
        # print(x1)
        if judge_a(a) == 1:
            exit()
        elif judge_a(a) == 2:
            final_point = x1
            break
        x2 = x1 + a * direction1

        ax3.scatter3D(x1[0, 0], x1[1, 0], bottom, c='g', s=scatter_size)
        ax3.plot((x1[0, 0], x2[0, 0]), (x1[1, 0], x2[1, 0]), (bottom, bottom), c='red')
        plt.pause(0.01)
        yield str('a1 = ') + str(abs(round(a, 2)))

        ax3.scatter3D(x2[0, 0], x2[1, 0], bottom, c='b', s=scatter_size)
        ax3.text(x2[0, 0], x2[1, 0], bottom, str((count + 1, 2)))
        plt.pause(0.01)
        yield str('x2 = ') + str((round(x2[0, 0], 2), round(x2[1, 0], 2)))

        a = GetA(function, x2, direction2)  # 计算步长，传进去的一定是方向，即负梯度
        if judge_a(a) == 1:
            exit()
        elif judge_a(a) == 2:
            final_point = x2
            break

        x3 = x2 + a * direction2

        ax3.scatter3D(x1[0, 0], x1[1, 0], bottom, c='g', s=scatter_size)
        ax3.scatter3D(x2[0, 0], x2[1, 0], bottom, c='g', s=scatter_size)
        ax3.plot((x3[0, 0], x2[0, 0]), (x3[1, 0], x2[1, 0]), (bottom, bottom), c='red')
        plt.pause(0.01)
        yield str('a2 = ') + str(abs(round(a, 2)))

        ax3.scatter3D(x3[0, 0], x3[1, 0], bottom, c='b', s=scatter_size)
        ax3.text(x3[0, 0], x3[1, 0], bottom, str((count + 1, 3)))
        plt.pause(0.01)
        yield str('x3 = ') + str((round(x3[0, 0], 2), round(x3[1, 0], 2)))

        direction3 = x3 - x1

        a = GetA(function, x3, direction3)
        if judge_a(a) == 1:
            exit()
        elif judge_a(a) == 2:
            final_point = x3
            break
        x1 = x3 + a * direction3

        ax3.plot((x1[0, 0], x3[0, 0]), (x1[1, 0], x3[1, 0]), (bottom, bottom), c='red')
        plt.pause(0.01)
        yield 'a3 = ' + str(abs(round(a, 2)))

        direction1 = direction2
        direction2 = direction3

        # plt.pause(0.01)
        # yield
        # ax3.scatter3D(x1[0, 0], x1[1, 0], bottom, c='g', s=scatter_size)

        good_results.append(x1)
        final_point = x1

        count += 1

    ax3.scatter3D(final_point[0, 0], final_point[1, 0],
                  bottom, c='r', label='最优点', s=scatter_size)
    plt.pause(0.01)

    if count == 0:
        count += 1
    print("一共迭代了{:}次\n极小值点为({:.2f},{:.2f})\n极小值为{:.2f}"
          .format(count, float(x1[0, 0]), float(x1[1, 0]), float(function(x1[0, 0], x1[1, 0]))))
    # print("x1 = ", good_results)
    yield 'result'
    yield ("一共迭代了{:}次\n极小值点为({:.2f},{:.2f})\n极小值为{:.2f}"
           .format(count, float(x1[0, 0]), float(x1[1, 0]), float(function(x1[0, 0], x1[1, 0]))))


    plt.show()


if __name__ == "__main__":
    display(x_range=(-5, 10), y_range=(-5, 7), function=fun3, X0=[-5, 4])
    # display((-5, 10), (-5, 7), fun3, X0=[-5, 4])  # fun4
