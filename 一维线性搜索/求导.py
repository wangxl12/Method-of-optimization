def first_derivative(fun, x, delta=0.0001):
    result = (fun(x + delta) - fun(x)) / delta
    return result


def second_derivative(fun, x, delta=0.0001):
    result = (first_derivative(fun, x + delta) - first_derivative(fun, x)) / delta
    return result
