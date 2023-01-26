from function_plotter_source_code import MainApp
import pytest

@pytest.fixture
def initializer():
    return MainApp()

@pytest.fixture
def executer():
    return MainApp().exec_()
   


def test_xlimits_validation(initializer, executer):
    MainApp.assigner()
    for MainApp.x_lim_left in [12.5 , 'two', '$']:   # some examples of invalid inputs
        assert MainApp.lbl_xlim_error.Text() == '❌ Only "Integer" values are Valid ❌'
    MainApp.plotter()
    for i , j in [(-2,2),(2,-2),(3,3)]:
        MainApp.x_lim_left = i
        MainApp.x_lim_right = j
        if (MainApp.x_lim_left >= MainApp.x_lim_right):
            assert MainApp.lbl_func_error.Text() == '❌ Left X-Limit must be "less than" Right X-Limit ❌'


def test_func_formula_validation(initializer,executer):   
    MainApp.plotter()
    if MainApp.y == eval("2x"):
        assert MainApp.lbl_func_error.Text == "❌ Fill the function formula like this example: 5*x^2 + 3*x ❌" 
    
