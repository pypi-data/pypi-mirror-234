from scipy.stats import t
from numpy import sqrt

def random_error_of_mean(std, num_samples, confidence):
    """
    Calculates the random uncertainty of the mean of a set of samples following the formula:

        t_n-1 * (σ_n-1 / √n)
    """
    return std * t.ppf(1 - (1-confidence)*0.5 + confidence, num_samples - 1) * sqrt(num_samples)

def student_t_n(degrees_of_freedom, confidence):
    """
    Returns the t_n,ɑ/2 coefficient for the given degree of freedom and confidence level.
    Exact same inputs and outputs as the cheat sheet table from year 1
    """
    return t.ppf(1 - (1-confidence)*0.5, degrees_of_freedom)
