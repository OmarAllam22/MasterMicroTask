#---- importing necessary packages:
from PySide2.QtWidgets import QApplication, QGridLayout, QDialog, QPushButton, QLabel, QLineEdit
from PySide2.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from numpy import *    # Instead of (import numpy as np) to allow for "sin(x)" instead of "np.sin(x)" as input
import sys


class MainApp(QDialog):
    def __init__(self):
        super().__init__()

    #---- Declaring necessary variables            
        self.setWindowTitle("Function Plotter App")

        self.figure  = plt.figure()                   # matplotlib object to display the plotted function
        self.canvas  = FigureCanvas(self.figure)      # object to render the matplotlib figure content
        self.toolbar = NavigationToolbar(self.canvas) # toolbar to add extra control to the plot canvas

        self.my_font = QFont("Calibri", 12,QFont.Bold) # setting font object to use in Label-Texts

        self.lbl_func_error = QLabel() # To display the error message to user when typing the function
        self.lbl_xlim_error = QLabel() # To display the error message to user when typing the xlimts
        
        self.lbl_xtext_1 = QLabel() # To display certain text on the GUI window
        self.lbl_xtext_2 = QLabel() # To display certain text on the GUI window
        self.lbl_xtext_1.setText("Your X_limits are from")
        self.lbl_xtext_2.setText("To")
        self.lbl_xtext_1.setFont(self.my_font)
        self.lbl_xtext_2.setFont(self.my_font)
        
        self.lbl_func_text = QLabel()
        self.lbl_func_text.setText("Type your function formula below:")
        self.lbl_func_text.setFont(self.my_font)

        self.button = QPushButton()
        self.button.setText("Click Here To Plot 📈")
        self.button.setFont(self.my_font)

        self.line_func   = QLineEdit() # To receive the user-input function formula
        self.line_xlim_l = QLineEdit() # To receive the user-input Left xlimit
        self.line_xlim_r = QLineEdit() # To receive the user-input Right xlimit

    #---- Plot the function using `plotter` function through two ways (click "Enter" or press the button): 
        self.line_func.returnPressed.connect(self.plotter)        
        self.button.clicked.connect(self.plotter)
        
    #---- Assign the user-input xlimits to certain variables using `assigner` function:
        self.line_xlim_l.editingFinished.connect(self.assigner)
        self.line_xlim_r.editingFinished.connect(self.assigner) 
    
    #---- Declare a Layout object of type "Grid" and addwidgets to it:
        # .addWidget() uses four numbers --> (row_index, col_index, num_of_spanned_rows, num_of_spanned_cols):
        layout = QGridLayout()

        layout.addWidget(self.lbl_xtext_1,  1,0, 1,1)    # to display "Your X_limits are from"
        layout.addWidget(self.line_xlim_l,  1,1, 1,1)    # to receive left xlimit
        layout.addWidget(self.lbl_xtext_2,  1,2, 1,1)    # to display "to"
        layout.addWidget(self.line_xlim_r,  1,3, 1,1)    # to receive right xlimit
        layout.addWidget(self.lbl_xlim_error,  2,0, 1,2) # to display any arised xlimits-related errors 
        layout.addWidget(self.canvas,  3,0, 4,4)         # to display the function graph
        layout.addWidget(self.toolbar,  7,2)             # to display the toolbar
        layout.addWidget(self.lbl_func_text,  7,0)       # to display "Type your function formula below:"
        layout.addWidget(self.line_func,  8,0, 1,4)      # to receive the function formula
        layout.addWidget(self.lbl_func_error)            # to display any arised function-related errors
        layout.addWidget(self.button,  10,0, 1,4)        # to display the plotting button
                
        self.setLayout(layout)

    #---- used-functions declaration:
    def assigner(self):
        """
        A funtion to :

            1. Assign the user-input left and right xlimits in the lineEdit to variables named:
                `self.x_lim_left` & `self.x_lim_right`
            2. Cast those variables to `integer` to be used later in matplotlib methods
            3. Validate both the two limits are entered by the user
            4. Validate both the limits are iputed as numerical integer values not otherwise  
        
        """
        
        self.lbl_xlim_error.setText("")  # Reset the label error-text at each new call for the function

        try:
            self.x_lim_left  = int(self.line_xlim_l.text().strip())
            self.x_lim_right = int(self.line_xlim_r.text().strip()) 

        except:
            if ( len(self.line_xlim_l.text().strip()) == 0 )  or ( len(self.line_xlim_r.text().strip()) == 0 ): 
                self.lbl_xlim_error.setText('⚠️ Note: Both X_limits must be specified ⚠️')
            else:
                self.lbl_xlim_error.setText('❌ Only "Integer" values are Valid ❌')

        
    def plotter(self):            
        """
        A funtion to :
            
            1. plot the function formula entered by the user
            2. set the plot-limits to the xlimits entered by the user
            3. Validate the entered formula follows the rules of 2*x instead 2x ...,etc
            4. Make a validation for either constant-function or x-dependent function
        
        """
        
        # Reset the label texts & figure at each new function call
        self.lbl_xlim_error.setText("")  
        self.lbl_func_error.setText("")  
        self.figure.clear()       
        
        try:
            if (self.x_lim_left >= self.x_lim_right) :
                self.lbl_func_error.setText('❌ Left X-Limit must be "less than" Right X-Limit ❌')
                return None
            
            x = linspace(self.x_lim_left,self.x_lim_right,1000)
        except:
            self.lbl_func_error.setText('❌ Check your X-Limits ❌')  # return here is to exit the function plotter incase of errors
            return None
        
        try:                
            # In order to plot constant functions like: f(x) = 5
            if self.line_func.text().strip().isdigit():
                self.y = eval(self.line_func.text() + "*x**0")
            
            else:
                self.y = eval(self.line_func.text().lower().replace("^","**"))

            self.ax = self.figure.add_subplot(111) # this method takes 3 parameters: (nrows, ncols, index) (111) means row:1, col:1, index:1
            self.ax.set_xlim(self.x_lim_left,self.x_lim_right)
            self.ax.plot(x,self.y)
            plt.axhline(y=0, color='k') # mark the x-axis as solid black line 
            plt.axvline(x=0, color='k') # mark the y-axis as solid black line
            plt.grid()                  # show grids to help inreading plot values

            self.canvas.draw()
        
        except:
            self.lbl_func_error.setText("❌ Fill the function formula like this example: 5*x^2 + 3*x ❌" )


# create an object of our GUI and start the event loop of the GUI:
app = QApplication(sys.argv)
win = MainApp()
win.show()
app.exec_()
