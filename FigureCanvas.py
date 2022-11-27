from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import random
import numpy as np
from collections import OrderedDict
plt.style.use("ggplot")


class Canvas(FigureCanvas): 
    def __init__(self, parent, comps_to_fit, data, fitted_data=None, log_scale=False): 
        self.fig, self.axs= plt.subplots(1,len(comps_to_fit))
        super().__init__(self.fig)
        self.setParent(parent)
        self.fitted_data = fitted_data
        self.data = data
        self.comps_to_fit = comps_to_fit
        self.log_scale = log_scale
        #self.colors_scatter = ["b", "g", "r", "c", "m", "y", "k"]
        #self.colors_line = ["b", "g", "r", "c", "m", "y", "k"]
        if fitted_data is None:
            self.show_data() 
        else: 
            self.show_fit()

    def show_fit(self): 
        
        if len(self.comps_to_fit) > 1: 
            for x, comp in enumerate(self.comps_to_fit):
                
                self.axs[x].scatter(np.linspace(0, self.data[comp].size-1, self.data[comp].size), self.data[comp], marker = 'o')  
                self.axs[x].set_title(self.comps_to_fit[x])
                self.axs[x].plot(np.linspace(0., self.data[comp].size-1, 1000), self.fitted_data[:,x], '-', linewidth = 2)
                if self.log_scale: 
                    self.axs[x].set_yscale("log", base=10)    
            
        else: 
            
            self.axs.scatter(np.linspace(0, self.data[self.comps_to_fit[0]].size-1, self.data[self.comps_to_fit[0]].size), self.data[self.comps_to_fit[0]], marker = 'o')  
            self.axs.set_title(self.comps_to_fit[0])
            self.axs.plot(np.linspace(0., self.data[self.comps_to_fit[0]].size-1, 1000), self.fitted_data[:,0], '-', linewidth = 2)
            if self.log_scale: 
                self.axs.set_yscale("log", base=10)
        
        plt.close(self.fig)
              
    def show_data(self): 
                     
        if len(self.comps_to_fit) > 1: 
            for x, comp in enumerate(self.comps_to_fit):
                self.axs[x].scatter(np.linspace(0, self.data[comp].size-1, self.data[comp].size), self.data[comp], marker = 'o')  
                self.axs[x].set_title(self.comps_to_fit[x])
                if self.log_scale: 
                    self.axs[x].set_yscale("log", base=10)
        else: 
            self.axs.scatter(np.linspace(0, self.data[self.comps_to_fit[0]].size-1, self.data[self.comps_to_fit[0]].size), self.data[self.comps_to_fit[0]], marker = 'o')  
            self.axs.set_title(self.comps_to_fit[0])
            if self.log_scale: 
                    self.axs.set_yscale("log", base=10)

        plt.close(self.fig)
            
   
class SingleCanvas(FigureCanvas): 
    def __init__(self, parent, comp, data, fitted_data=None, log_scale=False, interventions=None): 
        self.fig, self.axs= plt.subplots()
        super().__init__(self.fig)
        self.setParent(parent)
        self.comp = comp
        self.data = data
        self.fitted_data = fitted_data
        self.log_scale = log_scale
        self.interventions = interventions
        self.line_color = "tomato"
        self.scatter_color = "darkslategray"
        if fitted_data is None:
            self.show_data() 
        else: 
            if interventions is None: 
                self.show_fit()
            else: 
                self.show_fit_inter()
    
    def show_data(self): 
        self.axs.scatter(np.linspace(0, self.data.size-1, self.data.size), self.data, marker = 'o')  
        self.axs.set_title(self.comp)
        if self.log_scale: 
                self.axs.set_yscale("log", base=10)
        
        plt.close(self.fig)

    def show_fit(self): 
        self.axs.plot(np.linspace(0, self.data.size-1, self.data.size), self.data, 'o', color=self.scatter_color)  
        self.axs.set_title(self.comp)
        self.axs.plot(np.linspace(0., self.data.size-1, 1000), self.fitted_data, '-', linewidth = 2, color=self.line_color)
        if self.log_scale: 
            self.axs.set_yscale("log", base=10)   

        plt.close(self.fig) 
    
    def show_fit_inter(self): 

        self.axs.plot(np.linspace(0, self.data.size-1, self.data.size), self.data,'o', color=self.scatter_color)  
        self.axs.set_title(self.comp)
        intervs = self.interventions
        #self.axs.plot(np.linspace(0, self.data.size-1, self.fitted_data.size), self.fitted_data, '-', linewidth=2)
        for i in range(len(intervs)+1):
            if i==0: 
                self.axs.plot(np.linspace(0,intervs[0],1000), self.fitted_data[:1000], linewidth=2, color=self.line_color)
            elif i==len(intervs): 
                self.axs.plot(np.linspace(intervs[i-1], self.data.size, 1000), 
                        self.fitted_data[1000*i: 1000*(i+1)], linewidth=2, color=self.line_color)
            else: 
                self.axs.plot(np.linspace(intervs[i-1], intervs[i], 1000), 
                        self.fitted_data[1000*i: 1000*(i+1)],linewidth=2, color=self.line_color)
            if i<len(intervs): 
                self.axs.axvline(intervs[i], linestyle='dotted',color="black")

        if self.log_scale: 
            self.axs.set_yscale("log", base=10)
        plt.close(self.fig)