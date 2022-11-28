# Fitting-Tool
This project was initiated by Prof. Dr. Konstantinos Panagiotou to develop a program to compare a model based on differential equations with real data. The model can be created with the help of a website, which was also created by the professor's collaborators. This website can also be used to generate artificial data to test the program. 

## fitting_tool_new.py ##
This Python script is the starting point of the tool. The class "Ui_MainWindow" takes care of all tasks related to the creation and modification of the user interface. 

## fitting_tool_logic.py ## 
This script contains three functions in total. The function "Fit" takes care of the actual execution of the calculations. The functions "Get_Data" and "Get_Model" control the loading of the respective files into the user interface. 

## genfitalg.py ## 
This class takes a model and data and generally calculates those parameters of the model for which the Mean Square Error with respect to the data is as small as possible. This class is called by the "Fit" method. 

## find_interventions.py ## 
This class also calculates the mean square error between the model and the data, but takes into account the possible occurrence of parameter changes, i.e. so-called "interventions". The number of possible interventions must be defined by the user beforehand.

## FigureCanvas.py ## 
This script contains two classes whose objects are used in the script "fitting_tool_new.py" to draw the data on a matplotlib based canvas so that it can be displayed to the user. 
