from get_data import get_sir_data, get_seir_data, get_sis_data
import numpy as np
from scipy.signal import argrelmax
import matplotlib.pyplot as plt
from numpy import gradient
import time
import numpy as np
import genfitalg
import copy
from itertools import combinations
from scipy.ndimage import gaussian_filter
from collections import OrderedDict
from scipy import signal



class fit_model_to_data_intervention: 
    
    def __init__(self, json_data, num_intervs): 
        self.json_data = json_data
        self.model = json_data["Model"]
        self.num_intervs = num_intervs
        self.comps_to_fit = self.model["Compartments_to_Fit"]
        self.data = json_data["Data"]
        
        self.fit_report = ""
        self.current_fit_report = ""
        self.residual = 0
        
        # Generate Susceptible data if not provided by the user 
        if self.model['Susceptibles'] not in self.data.keys(): 
            susceptible_data = np.full(list(self.data.values())[0].shape[0], self.model["n"])
            for key in self.data.keys(): 
                if key == "n": 
                    continue
                susceptible_data = susceptible_data-self.data[key]
            self.data[self.model['Susceptibles']] = susceptible_data
            self.comps_to_fit.append(self.model['Susceptibles'])
    
        self.candidates_dict = {}
        self.combs_cand_dict = {}
        
        # Calculate first and second derivative in order to find good guesses for interventions
        for comp in self.comps_to_fit: 
            dcomp = gradient(self.data[comp])
            ddcomp = abs(gradient(dcomp))
            self.candidates_dict[comp] = argrelmax(ddcomp, order=6)[0]
            self.combs_cand_dict[comp] = list(combinations(self.candidates_dict[comp],self.num_intervs))
 
    def compute_fit(self, model, i): 
        # Compute the actual fit and store the results. 
        fit = genfitalg.fit_model_to_data(model)
        erg = fit.solve()
        self.residual += erg[1]
        self.current_fit_report += f"################################ Intervention {i} ################################\n"
        self.current_fit_report += erg[2]+"\n\n"
        return erg[0]

    def find_interventions_new(self, combs): 
        
        minimum = 10e+100
        interventions = None
        best_fit = None

        # For every combination of intervention points compute
        # the fits for every intervall and choose the combination with 
        # the smallest error sum. 
        for j, comb in enumerate(combs):
            comb = list(comb)
            comb.insert(0, 0)
            max_len = len(list(self.data.items())[0][1]) 
            comb.append(max_len)
            self.residual = 0
            self.current_fit_report = ""
            model = copy.deepcopy(self.json_data)
            
            for i in range(0, len(comb)-1):
                for comp in self.comps_to_fit: 
                    model["Data"][comp] = self.data[comp][comb[i]:comb[i+1]] 
                    model["Model"]["IV"][comp] = self.data[comp][comb[i]]
                if i == 0: 
                    fitted_data = self.compute_fit(model, 0)
                else: 
                    fitted_data = np.concatenate((fitted_data, self.compute_fit(model, i)))
   
            #print(f"Durchgang Nummer {j}")
            #print(f"Combination: {comb}")
            if self.residual < minimum: 
                self.fit_report = self.current_fit_report
                minimum = self.residual
                interventions = comb[1:len(comb)-1]
                best_fit = fitted_data
                
            #print(f"Error: {minimum}")
        return minimum, interventions, best_fit

    def solve(self): 

        self.solutions = {}
        minimum = 10e+100
        interventions = None
        best_fit = None
        fit_report = ""

        # For every Compartement to Fit calculate the best intervention points. 
        # Afterwards compare the best intervention points and choose the best one.
        # That's the solution of this calculation. 
        for comp in self.comps_to_fit: 
            self.solutions[comp] = self.find_interventions_new(self.combs_cand_dict[comp])
            #print(f"Interventions for {comp} compartment are at t= {self.solutions[comp][1]}")
            if self.solutions[comp][0] < minimum: 
                minimum = self.solutions[comp][0]
                interventions = self.solutions[comp][1]
                best_fit = self.solutions[comp][2]
                fit_report = self.fit_report 
                fit_report += "################################ Intervention(s) ##################################\n"
                fit_report += f"The intervention(s) are at t = {interventions}"
        
        #print(f"Interventions at t= {interventions}")
        with open("result.txt", "w") as text_file:
            text_file.write(fit_report)
       
        return interventions, best_fit






  


 





