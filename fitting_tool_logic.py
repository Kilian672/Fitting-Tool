from tkinter.messagebox import showerror
from tkinter import filedialog, messagebox
import json 
import os
import threading
import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np
from sympy.stats import Uniform, density
import random
import copy 
import genfitalg
import math
import find_interventions
from find_interventions import fit_model_to_data_intervention
from collections import OrderedDict

class NoSusException(Exception): 
    
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
def Fit(model, data, population, settings=None):
            
    try:

        # Delete all Nan-values
        data_to_fit = {"Data": {}}
        for comp in data: 
            data_to_fit["Data"][comp] = np.nan_to_num(data[comp], nan=0.0)
            
        data_to_fit["Model"] = copy.deepcopy(model)
        data_to_fit["Model"]["n"] = population
        
        
        #Handle initial value dictionary. (Very messy!)
        initial_value_dict = {}
        sum  = 0
        for comp in data_to_fit["Model"]["Compartments_to_Fit"]: 
            initial_value_dict[comp] = data_to_fit["Data"][comp][0]
            if comp != data_to_fit["Model"]["Susceptibles"] and comp != "n":
                sum = sum+data_to_fit["Data"][comp][0] 
        for comp in data_to_fit["Model"]["Equations"]: 
            if comp not in data_to_fit["Model"]["Compartments_to_Fit"]:
                if comp == data_to_fit["Model"]["Susceptibles"]: 
                    if comp not in data_to_fit["Model"]["Compartments_to_Fit"]: 
                        if "n" in data_to_fit["Model"]["Compartments_to_Fit"]: 
                            initial_value_dict[comp] = data_to_fit["Data"]["n"][0]-sum
                        else: 
                            initial_value_dict[comp] = data_to_fit["Model"]["n"]-sum
                elif comp == "n": 
                    if "n" not in data_to_fit["Model"]["Compartments_to_Fit"]: 
                        initial_value_dict[comp] = data_to_fit["Model"]["n"]       
                else:
                    initial_value_dict[comp] = 0         
        data_to_fit["Model"]["IV"] = copy.deepcopy(initial_value_dict)
        
        #Settings for the fitting-object. 
        attempts = settings["Attempts"]
        max_evals=settings["Max_Evals"]
        fitting_algorithm=settings["Fitting_Algorithm"]
        lower_bound = settings["Lower_Bound"]
        upper_bound = settings["Upper_Bound"]
        interventions = settings["Interventions"]
        
        #Solve the fitting-task with interventions
        #TODO: Use custom settings. 
        if interventions > 0: 
            fitting_object = fit_model_to_data_intervention(data_to_fit, interventions)
            return fitting_object.solve()
        

        initial_guess = {}
        minimum = 10e+100
        fitted_data = None
        fitted_data_report = ""

        #Try to fit the model to the data with different initial parameter-values. 
        #Choose the best fit (smallest MSE).
        for _ in range(max(1, attempts)):
            #Initialize the parameters at random (Unif(lower_bound, upper_bound))
            for param in data_to_fit["Model"]["Parameters"]:
                    initial_guess[param] = random.uniform(max(0,lower_bound),upper_bound)
            #Initialize the fitting-class with the model and the data specified by the user.
            fitting_object = genfitalg.fit_model_to_data(data_to_fit)
        
            try: 
                #Solve the fitting-task with custom settings.
                solution = fitting_object.solve(fitting_algorithm=fitting_algorithm, 
                                                    max_evals=max_evals, initial_guess=initial_guess, 
                                                        lower_bound=lower_bound, upper_bound=upper_bound)
            except ValueError: 
                continue
            except RuntimeWarning: 
                #print("A warning has been ignored!")
                continue 

            #Check if the algorithm found a better approximation. 
            current_minimum = solution[1]
            if current_minimum < minimum: 
                minimum = current_minimum 
                fitted_data = solution[0]
                fitted_data_report = solution[2]
                with open("result.txt", "w") as text_file:
                    text_file.write(fitted_data_report)
        
        return None, fitted_data
    
    except: 
        return 
    
def Get_Data(filename, read_data_file):
        
    var_data = {}
    try: 
        #Get the data for one compartement at a time. 
        for comp, column in read_data_file["Columns"].items(): 
            start = int(read_data_file["start_row"])
            stop = int(read_data_file["end_row"])
            try: 
                #Get the data for the compartement corresponding to the column specified by the user
                #and store it in a numpy-array. 
                new_data = genfromtxt(str(filename), delimiter=',', 
                                        skip_header=start, usecols=int(column)-1, max_rows=stop-start)
            except OSError: 
                return
            #Replace all the undefined values with zero. 
            new_data = np.nan_to_num(new_data, nan=0.0)
            var_data[comp] = new_data

        if var_data != {}:
            #Return the data as a dictionary.  
            return var_data
    except: 
        return

def Get_Model(filename):
 
    #Open the json-file specified by the user. 
    try: 
        with open(str(filename),'r') as file:
            model_file = json.load(file)
    except OSError: 
        return 

    model = model_file["Model"]
    
          
    model["state-names"]["n"] = "n"
    if model["state-names"]["s0"] == "": 
        raise NoSusException("Please specify a susceptible compartement.")
    
    state_names = copy.deepcopy(model["state-names"])
    rate_names = copy.deepcopy(model["rates-names"])
    
    #For some reason the class "Parameters" used in "genfitalg.py" doesn't want a variable to be called "lambda".
    #So in case there is a Parameter called "lambda" we change it to "LAMBDA". 
    for rate_name in rate_names.keys(): 
        if rate_names[rate_name] == "lambda": 
            rate_names[rate_name] = "LAMBDA"

    #Replace the compartement/parameter-ids given by EMD-download with their real names. 
    model["Parameters"] = []
    n_comp_string = "" 
    for key_eq in model["Equations"].keys():
        for key_stat in reversed(state_names.keys()): 
            model["Equations"][key_eq] = model["Equations"][key_eq].replace(key_stat, state_names[key_stat])
        for key_rat in rate_names.keys(): 
            model["Equations"][key_eq] = model["Equations"][key_eq].replace(key_rat, rate_names[key_rat])
            if rate_names[key_rat] not in model["Parameters"]: 
                model["Parameters"].append(rate_names[key_rat])
        if key_eq != "n": 
            n_comp_string = n_comp_string + model["Equations"][key_eq]
    model["Equations"]["n"] = n_comp_string
    
    #Order the equations starting with all the compartements for which there is data available.
    ordered_dict = OrderedDict()
    for i, comp in enumerate(model["Compartments_to_Fit"]): 
        ordered_dict[state_names[comp]] = model["Equations"][comp]
        model["Compartments_to_Fit"][i] = state_names[comp]
    for comp in model["Equations"]: 
        if comp not in model["Compartments_to_Fit"]: 
            ordered_dict[state_names[comp]] = model["Equations"][comp]
    
    #Replace the unordered equations with the ordered equations. 
    if ordered_dict != {}:
        model["Equations"] = copy.deepcopy(ordered_dict)
    model["Susceptibles"] = state_names[model["Susceptibles"]]
        
    #Delete all the information that we don´t need anymore.
    model.pop("rates-names")
    model.pop("state_ids")
    model.pop("state-names")
    #print(json.dumps(model, indent=2))
    
    #Return the model as a dictionary. 
    return model 
                


