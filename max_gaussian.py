from math import *

#fitting a Gaussian
def f(mu, sigma2, x):
    return 1/sqrt(2.*pi*sigma2) * exp(-.5*(x-mu)**2 / sigma2)


def update(mean1, var1, mean2, var2):
    """
    updating the Gaussian based upon a newly observed mean and sigma
    """
    new_mean = ( (var2 * mean1) + (var1 * mean2) ) / (var2 + var1) 
    new_var = 1 / ( (1/var2)  + (1/var1) )

    return [new_mean, new_var] 


def predict(mean1, var1, mean2, var2):
    """
    predict the new mean and variance after a motion, given a prior
    """
    new_mean = mean1 + mean2
    new_var = var1 + var2

    return [new_mean, new_var]



measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0
sig = 10000



for i in range(len(measurements)):
    [mu, sig] = update(mu, sig, measurements[i], measurement_sig)
    print "update:  ", [mu, sig]
    [mu, sig] = predict(mu, sig, motion[i], motion_sig)
    print "predict: ", [mu, sig]    