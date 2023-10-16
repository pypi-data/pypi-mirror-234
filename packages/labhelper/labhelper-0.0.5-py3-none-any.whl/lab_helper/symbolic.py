import sympy as sp
from IPython.display import display

sp.init_printing()

class Helper:
    """
    Helper class made to simplify the process of making a function programatically and to calculate the error function associated to the given function.
    
    In order to input LaTex symbols (such as greek letters, letters with subscripts or superscripts, such as t_0, or any other symbol which is valid in LaTex)
    the input must be written as it would be in LaTex: "ɑ_0" would be "\\alpha_{0}" (in the case of green letters the backslash "\\" can be ommited -> "\\alpha_{0}" = "alpha_{0}")
    
    MAKE SURE THAT THE PROVIDED VARIABLES IN vars_in, const_in MATCH EXACTLY WITH THE VARIABLES AND CONSTANTS IN THE FUNCTION
    """
    # For Readers looking at the documentation from source code keep in mind \\ is equivalent to \ because of the manner in which python parses docstrings
    def __init__(self, vars_in: list[str] , const_in: list[str], func_str: str, error_mark: str = "\Delta ") -> None:
        self.vars_text = vars_in
        self.vars = [sp.Symbol(e) for e in vars_in]
        self.consts_text = const_in
        self.consts = [sp.Symbol(e) for e in const_in]
        self.function = sp.parse_expr(func_str)
        
        if not all(item in self.function.atoms(sp.Symbol) for item in self.vars + self.consts):
            raise ValueError("The given variables and/or constants are not the same as in the given function")

        self.error_mark = error_mark
        self.errors_text = [self.error_mark + a for a in vars_in]
        self.errors = [sp.Symbol(a) for a in self.errors_text]
    
    def function_input_check(self):
        display(self.function.atoms(sp.Symbol))

    def display_data(self):
        print("Variables:")
        display(self.vars)
        print("Constants:")
        display(self.consts)
        print("Function:")
        display(self.function)
    
    def calculate_error_function(self):
        self.error_function = 0
        for i in range(len(self.consts_text)): 
            a = sp.Mul(self.errors[i], sp.diff(self.function, self.vars[i]), evaluate= False)
            b = sp.Pow(a, 2, evaluate=False)
            self.error_function = sp.Add(self.error_function, b)
        self.error_function = sp.sqrt(self.error_function)
        
    def evaluate_function(self, subs: dict, as_float: bool = False):
        return float(self.function.evalf(subs=subs)) if as_float else self.function.evalf(subs=subs)
    
    def evaluate_error_function(self, subs: dict, as_float: bool = False):
        return float(self.error_function.evalf(subs=subs)) if as_float else self.error_function.evalf(subs=subs)