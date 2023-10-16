'''' Useful funcs '''
import matplotlib.pyplot as plt
import numpy as np
from sympy import diff, lambdify
from RSFlib.Constants import PhysConst


def cart2pol(x, y):
    ''' Converts karthesian to cylindrial '''
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (rho, phi)


def fit_uncertainty(pcov):
    return np.sqrt(np.diag(pcov))


def uncertainty(data, NB=0, return_result=False, print_result=True, graph=None):

    '''' Funkce na výpočet nejistot '''
    if len(data) <= 1:
        raise TypeError("Data must have MORE elements than 1!")

    stud_koef = [0, 6.3, 4.3, 3.18, 2.78, 2.57, 2.45, 2.37, 2.31, 2.26, 2.2, 2.14, 2.09, 2.04, 2.00, 1.98, 1.96]

    n = len(data)

    if n <= 10:
        k = stud_koef[n - 1]
    elif n <= 12:
        k = stud_koef[10]
    elif n <= 15:
        k = stud_koef[11]
    elif n <= 20:
        k = stud_koef[12]
    elif n <= 30:
        k = stud_koef[13]
    elif n <= 60:
        k = stud_koef[14]
    elif n <= 120:
        k = stud_koef[15]
    else:
        k = stud_koef[16]

    xs = 1 / n * sum(data)  # střední hodnota
    sumx = 0

    for x in data:
        sumx = sumx + (x - xs) ** 2  # suma (xi - xs)**2

    sigma = np.sqrt(1 / (n * (n - 1)) * sumx)  # výpočet sigmy
    NA = k * sigma  # Nejistota typu A
    N = np.sqrt(NA ** 2 + NB ** 2)  # Výpočet nejistoty

    if print_result == True:
        print(f"x = ({xs:.5f} $\pm$ {N:.5f})")

    if graph != None:
        fig, ax = graph

        ax.plot(range(1, len(data) + 1), data, ".", color="black", label="Data")
        ax.plot(range(1, len(data) + 1), [xs]*len(data), "-", color="red", label="Mean")
        ax.plot(range(len(data) + 2), [xs + N] * (len(data) + 2), "--", color="green", label="Stdev")
        ax.plot(range(len(data) + 2), [xs - N] * (len(data) + 2), "--", color="green")

    if return_result == True:
        return (xs, N)


def GetMinIndex(inputlist):
    '''get index of the minimum value in the list'''
    min_value = min(inputlist)

    # return the index of minimum value

    min_index = []

    for i in range(0, len(inputlist)):

        if min_value == inputlist[i]:
            min_index.append(i)

    return min_index


def max_diff(data):
    '''Function that returns biggest difference in dataset'''
    max_difference = float("-inf")  # Initialize max_difference to negative infinity

    for i, value in enumerate(data):
        diff = abs(value - i)  # Calculate the difference between value and index
        max_difference = max(max_difference, diff)  # Update max_difference

    return max_difference


def log_b(a, base):
    ''' logaritm from a of base b'''
    return np.log(a) / np.log(base)


def cauchy(xdata, A=0, B=0, C=0):
    '''Cauchy function, returns ydata'''
    ydata = A + B/xdata**2 + C/xdata**4
    return ydata


def gauss(xdata, A=1, x0=0, sigma=0.1):
    '''Gauss function, returns ydata'''
    ydata = A * np.exp(-(xdata-x0)**2/(2*sigma**2))
    return ydata


def err_prop(func, variables, values, deviations):
    ''' error propagation deviation calculation function'''

    values_dict = {}
    for var, val in zip(variables, values):
        values_dict[str(var)] = val

    y_dev = 0
    for var, dev in zip(variables,deviations):
        derivative = diff(func, var)
        f = lambdify(variables, derivative)
        y_dev += (f(**values_dict)*dev)**2

    return np.sqrt(y_dev)

def calculate_perm(n, k):
    ''' function that makes permitivity from refractive index and absor '''

    epsilon1 = n**2 - k**2
    epsilon2 = 2 * n * k
    return epsilon1, epsilon2

def calculate_nk(epsilon1, epsilon2):
    ''' function that makes nk from permitivity '''

    n = np.sqrt((epsilon1 + np.sqrt(epsilon1**2 + epsilon2**2)) / 2)
    k = np.sqrt((np.sqrt(epsilon1**2 + epsilon2**2) - epsilon1) / 2)
    return n, k

def Ev2m(data):
    ''' calculates Ev to m '''
    pc = PhysConst()
    h, e, c = pc.planck, pc.elem_charge, pc.light_speed
    return h*c/data/e

def elips_eps(psi, delta, theta):
    ''' calculates complex dielectric function from psi, delta and theta, must be in radians '''
    rho = np.tan(psi) * np.exp(1j * delta)
    eps = np.sin(theta) ** 2 * (1 + ((1 - rho) / (1 + rho)) ** 2 * np.tan(theta) ** 2)
    return eps