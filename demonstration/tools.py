import sympy as sy
import numpy as np


def FirstDerivative(x, y, fun, delta=0.0001):
    """get the first derivative of the function at (x, y)
    :return first derivative
    :param x: the x value
    :param y: the y value
    :param fun: the function
    :param delta:
    """
    dx = (fun(x + delta, y) - fun(x, y)) / delta
    dy = (fun(x, y + delta) - fun(x, y)) / delta
    return np.array([dx, dy])


def SecondDerivative(x, y, fun, delta=0.0001):
    """get the second derivative of the function at (x, y)
    :return second derivative
    :param x: the x value
    :param y: the y value
    :param fun: the function
    :param delta:
    """
    dx2 = (FirstDerivative(x + delta, y, fun)[0] -
           FirstDerivative(x, y, fun)[0]) / delta
    dxdy = (FirstDerivative(x, y + delta, fun)[0] -
            FirstDerivative(x, y, fun)[0]) / delta
    dydx = (FirstDerivative(x + delta, y, fun)[1] -
            FirstDerivative(x, y, fun)[1]) / delta
    dy2 = (FirstDerivative(x, y + delta, fun)[1] -
           FirstDerivative(x, y, fun)[1]) / delta
    # dx2 = first_derivative(first_derivative(x, y, fun)[0], first_derivative(x, y, fun)[0], fun)
    # dy2 = first_derivative(first_derivative(x, y, fun)[1], first_derivative(x, y, fun)[1], fun)
    # dxdy = first_derivative(first_derivative(x, y, fun)[0], first_derivative(x, y, fun)[1], fun)
    # dydx = first_derivative(first_derivative(x, y, fun)[1], first_derivative(x, y, fun)[0], fun)

    return np.array([[dx2, dxdy], [dydx, dy2]])


def GetA(fun, x, direction, coordinate_rotation=False):
    """x1 = x0 - a * grad,return best step a
    :param coordinate_rotation: only coordinates rotation method do not need a > 0
    :param fun:
    :param x:
    :param direction:
    :return: best step
    """
    if x.shape != (2,) or direction.shape != (2,):
        x = x.reshape(-1, )
        direction = direction.reshape(-1, )
    # print(x, "\t", grad)
    # print("x = ", x, " \t grad = ", grad)
    a = sy.Symbol('a', real=True)  # real表示去除复数根
    # print(x[0] + a * direction[0], '\t', x[1] + a * direction[1])
    fun = fun(x[0] + a * direction[0], x[1] + a * direction[1])  # 关于a的函数
    # print(fun)
    diff_fun = sy.diff(fun, a)  # 求一阶导
    # print(diff_fun)
    # !!!!!!!!!!如果遇到解出来的a的值有多个该怎么办？！！！！！！！！！！！！！！！！
    # print(sy.solve(diff_fun, a))
    for value in sy.solve(diff_fun, a):
        if not coordinate_rotation:  # 如果不是坐标轮换法
            return value
        else:  # 如果是坐标轮换法
            return value
    return None


def GetInverseMatrix(matrix):
    """
    :param matrix: the matrix which will get its inverse matrix
    :return: the inverse matrix(two dimensions only)
    """
    matrix[0, 0], matrix[1, 1] = -matrix[1, 1], -matrix[0, 0]
    matrix = matrix / -(matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0])
    return matrix


def GetTransposeMatrix(matrix):
    """
    get the transpose matrix of the input matrix
    :param matrix:
    :return: the transpose matrix
    """
    first_dimension = matrix.shape[0]
    if first_dimension == 1:
        return matrix
    elif first_dimension == 2:
        matrix = np.array(list(zip(matrix[0], matrix[1])))
    elif first_dimension == 3:
        matrix = np.array(list(zip(matrix[0], matrix[1], matrix[2])))
    return matrix


def GetMagnitude(vector):
    """
    compute the magnitude of a vector
    :param vector: vector
    :return: value of the vector
    """
    vector = np.array(vector).reshape(-1, )
    magnitude = 0
    for vec in vector:
        magnitude += vec ** 2

    # magnitude = magnitude ** 0.5
    return magnitude


def MatrixPositiveDetermine(matrix):
    """
    determine if the matrix is positive
    :param matrix:
    :return: bool
    """
    shape_1 = np.array(matrix).shape[0]
    for i in range(1, shape_1 + 1):
        if np.linalg.det(matrix[: i, : i]) > 0:
            continue
        else:
            return False
    return True
