import numpy as np
from scipy.stats import f
from numba import jit, njit


def polyfit(data :np.ndarray,
            deg: int):

    x = np.arange(0, len(data))
    coefficients = np.polyfit(x, data, deg=deg)
    poly_function = np.poly1d(coefficients)
    print(poly_function)
    residuals = data - poly_function(x)
    degrees_of_freedom = len(x) - len(coefficients)
    y_hat = poly_function(x)
    SSR = np.sum((y_hat - np.mean(data)) ** 2)
    SSE = np.sum(residuals ** 2)
    f_statistic = (SSR / 2) / (SSE / degrees_of_freedom)
    return f_statistic

#@jit(nopython=True)
@njit('(float32[:], int64)')
def polyfit_numba(data: np.ndarray,
                  deg: int):

    x = np.arange(0, len(data)).astype(np.float32)
    mat_ = np.zeros(shape=(x.shape[0],deg + 1), dtype=np.float64)
    const = np.ones_like(x)
    mat_[:, 0] = const
    mat_[:, 1] = x
    if deg > 1:
        for n in range(2, deg + 1):
            mat_[:, n] = x ** n
    det_ = np.linalg.lstsq(mat_.astype(np.float32), data.astype(np.float32))[0][::-1]

    poly_function = np.zeros(x.shape)
    for degree, coef in enumerate(det_):
        r = coef * (x ** degree)
        poly_function = poly_function + r
    print(poly_function)






# y_fit = a * data ** 2 + b * data + c  # Fitted values
    # residuals = t - y_fit  # Residuals
    # mse = np.sum(residuals ** 2) / (len(t) - 3)  # Mean squared error (degrees of freedom = n - number of coefficients)
    # se_a = np.sqrt(mse / np.sum((data - np.mean(data)) ** 2))
    # df = n - len()


data = np.array([2, 4, 6, 7, 10]).astype(np.float32)
y = polyfit(data=data, deg=1)
y = polyfit_numba(data=data, deg=1)