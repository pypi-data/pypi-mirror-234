import numpy as np
import matplotlib.pyplot as plt


def transpose(mat):
    r = range(len(mat[0]))
    temp = [[] for _ in r]
    for col in mat:
        for i in r:
            temp[i].append(col[i])
    return temp


def sigmoid_(z):
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    temp = sigmoid_(z)
    return temp * (1 - temp)


def log_of_sigmoid_(z):
    return np.log(sigmoid_(z))


def log_of_sigmoid_prime(z):
    return 1 - sigmoid_(z)


def sinc_(z):
    return np.sinc(z)


def sinc_prime(z):
    if z == 0:
        return 0
    else:
        z *= np.pi
        return (np.cos(z) * z - np.sin(z)) / z ** 2


def gaussian_(z):
    return np.exp(-z ** 2)


def gaussian_prime(z):
    return np.exp(-z ** 2) * -2 * z


def softmax_(z):
    return np.exp(z)


def softmax_prime(z):
    return np.exp(z)


def tanh_(z):
    return 2 * sigmoid_(2 * z) - 1


def tanh_prime(z):
    return 2 * sigmoid_prime(z)


def arctan_(z):
    return np.arctan(z)


def arctan_prime(z):
    return 1 / (1 + z ** 2)


def ReLU_(z):
    if z > 0:
        return z
    else:
        return 0


def ReLU_prime(z):
    if z > 0:
        return 1.0
    else:
        return 0.0


def leaky_ReLU_(z, n_slope=0.25):
    if z > 0:
        return z
    else:
        return n_slope * z


def leaky_ReLU_prime(z, n_slope=0.25):
    if z > 0:
        return 1.0
    else:
        return n_slope


def swish_(z):
    return z / (1 + np.exp(-z))


def swish_prime(z):
    temp = sigmoid_(z)
    return temp * (z * (1 - temp) + 1)


def mish_(z):
    return z * tanh_(softplus_(z))


def mish_prime(z):
    return tanh_(softplus_(z)) + z * tanh_prime(softplus_(z)) * softplus_prime(z)


def softsign_(z):
    return z / (1 + abs(z))


def softsign_prime(z):
    if z > 0:
        return 1 / (z + 1) ** 2
    else:
        return 1 / (z - 1) ** 2


def softplus_(z):
    return np.log(1 + np.exp(z))


def softplus_prime(z):
    return sigmoid_(z)


def ELU_(z):
    if z < 0:
        return np.exp(z) - 1
    else:
        return z


def ELU_prime(z):
    if z < 0:
        return np.exp(z)
    else:
        return 1


def CrossEntropyCost_(x, y=0.5):
    return np.sum(np.nan_to_num(-y * np.log(x) - (1 - y) * np.log(1 - x)))


def CrossEntropyCost_prime(x, y=0.5):
    return -y / x + (1 - y) / (1 - x)


def QuadraticCost_(x, y=0):
    return (x - y) ** 2 / 2


def QuadraticCost_prime(x, y=0):
    return x - y


def plot_func(funcs, func_names=None, xl=-8, xh=8, density=10):
    if func_names is None:
        func_names = []
    elif type(func_names) != list:
        func_names = [func_names]
    if type(funcs) != list:
        funcs = [funcs]
    f = len(funcs)
    ln = len(func_names)
    if ln < f:
        for x in range(1, f - ln + 1):
            func_names.append("function" + str(x))
    x = []
    d = 1 / density
    for m in range(int(np.ceil((xh - xl) * density))):
        x.append(xl + m * d)
    for func in zip(funcs, func_names):
        y = []
        for x0 in x:
            y.append(func[0](x0))
        plt.plot(x, y, label=func[1])
        plt.legend()
    plt.show()


sigmoid = [sigmoid_, sigmoid_prime, "sigmoid"]  # outputs something close to 1 when positive, close to 0 when negative
softmax = [softmax_, softmax_prime, "softmax"]
gaussian = [gaussian_, gaussian_prime, "gaussian"]  # outputs 1 if inputs 0, outputs 0 if input is far from 0
sinc = [sinc_, sinc_prime, "sinc"]  # an alternative for gaussian
log_of_sigmoid = [log_of_sigmoid_, log_of_sigmoid_prime,
                  "log of sigmoid"]  # 0 when positive, itself when negative, no sharp points
arctan = [arctan_, arctan_prime, "arctan"]  # outputs something close to 1.5 when positive, close to 1.5 when negative
tanh = [tanh_, tanh_prime, "tanh"]  # outputs something close to one when positive, close to negative one when negative
ReLU = [ReLU_, ReLU_prime, "ReLU"]  # 0 if negative, itself if positive
leaky_ReLU = [leaky_ReLU_, leaky_ReLU_prime, "leaky ReLU"]  # itself scaled down if negative, itself if positive
swish = [swish_, swish_prime, "swish"]  # an alternative for ReLU: harder to calculate but better
linear = [lambda z: z, lambda z: 1, "linear"]  # outputs the input, typically used for linear regression
softsign = [softsign_, softsign_prime, "softsign"]  # an alternative for tanh: harder to calculate but better
softplus = [softplus_, softplus_prime, "softplus"]  # an alternative for ReLU: harder to calculate but better
ELU = [ELU_, ELU_prime, "ELU"]  # an alternative for ReLU: harder to calculate but better
# softmax, maxout layer
CrossEntropyCost = [CrossEntropyCost_, "Cross Entropy", CrossEntropyCost_prime]
QuadraticCost = [QuadraticCost_, "Quadratic", QuadraticCost_prime]
activate_dict = {"sigmoid": sigmoid, "gaussian": gaussian, "sinc": sinc, "softmax": softmax,
                 "tanh": tanh, "arctan": arctan, "log of sigmoid": log_of_sigmoid,
                 "ReLU": ReLU, "leaky ReLU": leaky_ReLU, "linear": linear,
                 "softsign": softsign, "softplus": softplus, "ELU": ELU, "swish": swish}
loss_dict = {"Cross Entropy": CrossEntropyCost, "Quadratic": QuadraticCost}


def array_operation(x, m, operation=lambda a, b: a + b):  # tested
    if type(x) != list:
        return operation(x, m)
    return [array_operation(v, w, operation) for v, w in zip(x, m)]
