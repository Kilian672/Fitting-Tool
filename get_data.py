from numpy import genfromtxt
import numpy as np
import standard_models


"""
                    Vorteil:                Nachteil: 
powell:             schnelle Berechnung,    unzuverlässig, 
                    gute Ergebnisse         sehr vom Anfangswert abhängig

dual_annealing: 

slsqp: 

""" 


"""'leastsq': Levenberg-Marquardt (default)
'least_squares': Least-Squares minimization, using Trust Region Reflective method
'differential_evolution': differential evolution
'brute': brute force method
'basinhopping': basinhopping
'ampgo': Adaptive Memory Programming for Global Optimization
'nelder': Nelder-Mead
'lbfgsb': L-BFGS-B
'powell': Powell
'cg': Conjugate-Gradient
'newton': Newton-CG
'cobyla': Cobyla
'bfgs': BFGS
'tnc': Truncated Newton
'trust-ncg': Newton-CG trust-region
'trust-exact': nearly exact trust-region
'trust-krylov': Newton GLTR trust-region
'trust-constr': trust-region for constrained optimization
'dogleg': Dog-leg trust-region
'slsqp': Sequential Linear Squares Programming
'emcee': Maximum likelihood via Monte-Carlo Markov Chain
'shgo': Simplicial Homology Global Optimization
'dual_annealing': Dual Annealing optimization"""


def get_sir_data(max_rows): 
     
    sus = genfromtxt("SIR_INT.csv", delimiter=',', skip_header=1, usecols=1, max_rows=max_rows)
    inf = genfromtxt("SIR_INT.csv", delimiter=',', skip_header=1, usecols=2, max_rows=max_rows)
    rec = genfromtxt("SIR_INT.csv", delimiter=',', skip_header=1, usecols=3, max_rows=max_rows)
    data = np.zeros((sus.shape[0], 3))
    data[:, 0] = sus
    data[:, 1] = inf
    data[:, 2] = rec
    return data

def get_sird_data(max_rows): 

    sus = genfromtxt("SIRD_INT.csv", delimiter=',', skip_header=1, usecols=1, max_rows=max_rows)
    inf = genfromtxt("SIRD_INT.csv", delimiter=',', skip_header=1, usecols=2, max_rows=max_rows)
    rec = genfromtxt("SIRD_INT.csv", delimiter=',', skip_header=1, usecols=3, max_rows=max_rows)
    dea = genfromtxt("SIRD_INT.csv", delimiter=',', skip_header=1, usecols=4, max_rows=max_rows)
    data = np.zeros((sus.shape[0], 4))
    data[:, 0] = sus
    data[:, 1] = inf
    data[:, 2] = rec
    data[:, 3] = dea
    return data

def get_seir_data(max_rows): 

    sus = genfromtxt("SEIR_INT.csv", delimiter=',', skip_header=1, usecols=1, max_rows=max_rows)
    exp = genfromtxt("SEIR_INT.csv", delimiter=',', skip_header=1, usecols=2, max_rows=max_rows)
    inf = genfromtxt("SEIR_INT.csv", delimiter=',', skip_header=1, usecols=3, max_rows=max_rows)
    rec = genfromtxt("SEIR_INT.csv", delimiter=',', skip_header=1, usecols=4, max_rows=max_rows)
    data = np.zeros((sus.shape[0], 4))
    data[:, 0] = sus
    data[:, 1] = exp
    data[:, 2] = inf
    data[:, 3] = rec
    return data

def get_seirs_data(max_rows): 

    sus = genfromtxt("SEIRS_INT.csv", delimiter=',', skip_header=1, usecols=1, max_rows=max_rows)
    exp = genfromtxt("SEIRS_INT.csv", delimiter=',', skip_header=1, usecols=2, max_rows=max_rows)
    inf = genfromtxt("SEIRS_INT.csv", delimiter=',', skip_header=1, usecols=3, max_rows=max_rows)
    rec = genfromtxt("SEIRS_INT.csv", delimiter=',', skip_header=1, usecols=4, max_rows=max_rows)
    data = np.zeros((sus.shape[0], 4))
    data[:, 0] = sus
    data[:, 1] = exp
    data[:, 2] = inf
    data[:, 3] = rec
    return data

def get_sis_data(max_rows): 
    
    sus = genfromtxt("SIS_INT.csv", delimiter=',', skip_header=1, usecols=1, max_rows=max_rows)
    inf = genfromtxt("SIS_INT.csv", delimiter=',', skip_header=1, usecols=2, max_rows=max_rows)
    data = np.zeros((sus.shape[0], 2))
    data[:, 0] = sus
    data[:, 1] = inf
    return data

def get_sirs_data(max_rows): 
     
    sus = genfromtxt("SIRS_INT.csv", delimiter=',', skip_header=1, usecols=1, max_rows=max_rows)
    inf = genfromtxt("SIRS_INT.csv", delimiter=',', skip_header=1, usecols=2, max_rows=max_rows)
    rec = genfromtxt("SIRS_INT.csv", delimiter=',', skip_header=1, usecols=3, max_rows=max_rows)
    data = np.zeros((sus.shape[0], 3))
    data[:, 0] = sus
    data[:, 1] = inf
    data[:, 2] = rec
    return data

def get_sir_model():
    #standard_models.sir_model
    #{"s": "-beta*s*i/n", "i": "beta*s*i/n-gamma*i", "r": "gamma*i"}
    model_dict = {"Equations": standard_models.sir_model, 
              "Parameters": ['beta', 'gamma'],
              "Compartments": ['s','i','r'],
              "Standard": 1} 
    return model_dict 

def get_sird_model(): 
    #{"s": "-beta*s*i/n", "i": "beta*s*i/n-gamma*i-delta*i", "r": "gamma*i", "d": "delta*i"}
    model_dict = {"Equations": standard_models.sird_model, 
              "Parameters": ['beta', 'gamma', 'delta'],
              "Compartments": ['s','i','r','d'],
              "Standard": 1}
    return model_dict

def get_seir_model(): 
    #standard_models.seir_model
    #{"s": "-beta*s*i/n", "e": "beta*s*i/n-epsilon*e", "i": "epsilon*e-gamma*i", "r": "gamma*i"}
    model_dict = {"Equations":standard_models.seir_model, 
              "Parameters": ['beta', 'epsilon','gamma'],
              "Compartments": ['s','e','i','r'],
              "Standard": 0}
    return model_dict

def get_sis_model():
    #{"s": "-beta*s*i/n+gamma*i", "i": "beta*s*i/n-gamma*i"}
    model_dict = {"Equations": standard_models.sis_model, 
              "Parameters": ['beta', 'gamma'],
              "Compartments": ['s','i'], 
              "Standard": 1} 
    return model_dict 

def get_sirs_model():
    
    model_dict = {"Equations": standard_models.sirs_model, 
              "Parameters": ['beta', 'gamma', 'tau'],
              "Compartments": ['s','i','r'],
              "Standard": 1} 
    return model_dict 

def get_seirs_model(): 
    
    model_dict = {"Equations": standard_models.seirs_model, 
              "Parameters": ['beta', 'epsilon','gamma', 'tau'],
              "Compartments": ['s','e','i','r'],
              "Standard": 1}
    return model_dict