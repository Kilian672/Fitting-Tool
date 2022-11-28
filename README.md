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

## thread_handling_classes.py ##
This script contains two classes that are used to create an additional thread (besides the main tread) that controls the elaborate calculations necessary to fit the model parameters to the data. 

## fitting_tool_ui.ui ## 
Diese Datei wurde mit dem sogenannten QtDesigner erstellt. Diese Datei kann in eine Python Datei umgewandelt werden und generiert automatisch den Code, der notwendig ist um die Benutzerschnittstelle zu zeichnen. Der entsprechende Befehl für die Erstellung der Python Datei ist "python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py"

## additional information ## 
The scripts "get_data.py" and "standard_models.py" are not used by the other functions and were only used to test the code. 
