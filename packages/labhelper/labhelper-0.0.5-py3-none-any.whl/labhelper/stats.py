from scipy.stats import t
from pandas import Series
import numpy as np

def random_error_of_mean(std, num_samples, confidence):
    """
    Calculates the random uncertainty of the mean of a set of samples following the formula:

        t_n-1 * (σ_n-1 / √n)
    """
    return std * t.ppf(1 - (1-confidence)*0.5 + confidence, num_samples - 1) * np.sqrt(num_samples)

def student_t_n(degrees_of_freedom, confidence):
    """
    Returns the t_n,ɑ/2 coefficient for the given degree of freedom and confidence level.
    Exact same inputs and outputs as the cheat sheet table from year 1
    """
    return t.ppf(1 - (1-confidence)*0.5, degrees_of_freedom)

def coefficient_errors(cov):
    return np.sqrt(np.diag(cov))

def bootstrap_points(x: list[float] | Series, y: list[float] | Series, xerr: list[float], yerr: list[float], num: int, keep_originals: bool = False, full_confidence: bool = False):
    if len(x) != len(y):
        raise ValueError("Lengths of x and y do not match!")
    if len(x) != len(xerr):
        raise ValueError("Lengths of x and xerr do not match!")
    if len(y) != len(yerr):
        raise ValueError("Lengths of y and yerr do not match!")

    xgen, ygen = [list(np.random.normal(xi, xierr * 0.5, num)) for xi, xierr in zip(x, xerr)], [list(np.random.normal(yi, yierr * 0.5, num)) for yi, yierr in zip(y, yerr)]
    xgen, ygen = sum(xgen, []), sum(ygen, []) # combine lists into one list
    if keep_originals:
        if type(x) == Series and type(y) == Series:
            xgen, ygen = x.to_list() + xgen, y.to_list() + ygen
        else:
            xgen, ygen = x.append(xgen), y.append(ygen)
    return xgen, ygen

