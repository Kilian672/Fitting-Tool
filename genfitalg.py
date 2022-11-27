from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from lmfit import minimize, Parameters, Parameter, report_fit, fit_report
from lmfit.model import save_modelresult
from scipy.integrate import odeint
from numpy import genfromtxt
import random 
import copy
from math import *
from collections import OrderedDict

class fit_model_to_data: 
    
    def __init__(self, json_data): 
        
        self.json_data = json_data
        self.equations = self.json_data["Model"]["Equations"]
        self.parameters = self.json_data["Model"]["Parameters"]
        self.initial_values = self.json_data["Model"]["IV"]
        self.population = self.json_data["Model"]["n"]
        self.fitting_comps = self.json_data["Model"]["Compartments_to_Fit"]
        self.initial_guess = None
        # list of all compartements
        self.compartements = list(self.equations.keys())
        # dictionary of all variables (compartements and parameters)
        self.variables_list = self.compartements+self.parameters
        self.variables_dict = {self.variables_list[i]: 0 for i in range(len(self.variables_list))}
        self.variables_dict["exp"] = exp 
        self.variables_dict["sqrt"] = sqrt
        self.variables_dict["atan"] = atan
        
        # initialize array with all the available data
        rows = self.json_data["Data"][self.fitting_comps[0]].size
        columns = len(self.json_data["Data"])
        self.data = np.zeros((rows, columns))
        for i, comp in enumerate(self.fitting_comps):
            self.data[:,i] = self.json_data["Data"][comp]
       
    # right hand side of the ode
    def f(self, X_t, t, paras):
        
        erg_list = []
        if "n" not in self.fitting_comps:
            n = self.population
        
        # change the parameter values accordingly
        for param in self.parameters:   
            self.variables_dict[param] = paras[param].value
        
        # change the values of the compartements accordingly
        for i, comp in enumerate(self.compartements): 
            self.variables_dict[comp] = X_t[i]

        # update equations using the updated compartement/parameter values  
        for comp in self.compartements: 
                erg_list.append(eval(self.equations[comp], self.variables_dict))
        return erg_list   
       
    # solve ode
    def g(self, t, x0, paras):

        x = odeint(self.f, x0, t, args = (paras, ))
        return x
    
    # auxiliary function needed in order to call "lmfit.minimize" in "self.solve_and_plot"
    def residual(self, paras, t, data):
        
        # save initial values in x0-list
        x0 = []
        for comp in self.compartements: 
            x0.append(paras[comp].value)

        # solve ode 
        model = self.g(t, x0, paras)

        # get only the data from the compartements we want to fit
        fitting_comps_model = model[:,0:len(self.fitting_comps)]
        
        # return the current error between actual data and estimated data
        return (fitting_comps_model - data).ravel()


    # solve the fitting task   
    def solve(self, fitting_algorithm='least_squares', max_evals=1000, upper_bound=1, lower_bound=0, initial_guess=None): 
        
        # list of time points
        self.number_of_datapoints = self.data.shape[0]
        self.t_measured = np.linspace(0,self.number_of_datapoints-1, self.number_of_datapoints)
       
        # define initial values and model parameters
        params = Parameters()
        initial_value_list = []
        # initial values
        for comp in self.compartements: 
            params.add(comp, value=self.initial_values[comp], vary=False)
            initial_value_list.append(self.initial_values[comp])
        # model parameters
        for param in self.parameters:
            if initial_guess is None:
                params.add(param, value = 1, max=upper_bound, min=max(0,lower_bound))
            else: 
                params.add(param, value = initial_guess[param], max=upper_bound, min=max(0,lower_bound))
            
        # fit model to data using "lmfit.minimize"-function
        result = minimize(self.residual, params, args = (self.t_measured, self.data), 
                                method=fitting_algorithm, max_nfev = max_evals)
        
        # solve ode with estimated parameters values (maybe replace 1000 with something, that depends on self.data.size)
        self.data_fitted = self.g(np.linspace(0., self.number_of_datapoints-1, 1000), initial_value_list, result.params)

        # return array of fitted data, the error of the fit (MSE-error) and some statistics calculated during the fit
        return [self.data_fitted[:,0:len(self.fitting_comps)], result.chisqr, fit_report(result)]


    

