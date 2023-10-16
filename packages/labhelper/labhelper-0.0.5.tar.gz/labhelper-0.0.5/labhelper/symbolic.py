from sympy import (Symbol, Mul, Add, Pow, diff, sqrt, parse_expr, solve, Equality, init_printing)
from IPython.display import display

init_printing()

def list_swap(l: list, x, y):
    if x not in l or y not in l:
        ValueError("elements not in given list!")
    el = [l.index(x), l.index(y)]
    l[el[0]], l[el[1]] = l[el[1]], l[el[0]]

class Helper:
    """
    Helper class made to simplify the process of making a function programatically and to calculate the error function associated to the given function.
    
    In order to input LaTex symbols (such as greek letters, letters with subscripts or superscripts, such as t_0, or any other symbol which is valid in LaTex)
    the input must be written as it would be in LaTex: "ɑ_0" would be "\\alpha_{0}" (in the case of green letters the backslash "\\" can be ommited -> "\\alpha_{0}" = "alpha_{0}")
    
    MAKE SURE THAT THE PROVIDED VARIABLES IN vars_in, const_in MATCH EXACTLY WITH THE VARIABLES AND CONSTANTS IN THE FUNCTION
    """
    # For Readers looking at the documentation from source code keep in mind \\ is equivalent to \ because of the manner in which python parses docstrings
    def __init__(self, func_str: str, vars_in: list[str] , const_in: list[str] = [], error_mark: str = r"\Delta ") -> None:
        self._vars_text = vars_in
        self._vars: list[Symbol] = [Symbol(e) for e in vars_in]
        self._consts_text = const_in
        if const_in:
            self._consts: list[Symbol] = [Symbol(e) for e in const_in]
        else:
            self._consts: list[Symbol] = []

        self._error_mark: str = error_mark
        self._errors_text: list[str] = [self._error_mark + a for a in vars_in]
        self._error_function = 0
        self._errors: list[Symbol] = [Symbol(a) for a in self._errors_text]

        all_vars: list[Symbol] = self._vars + self._consts
        text: list[str] = vars_in + const_in
        [list_swap(text, x, y) for x in text for y in text if x in y and text.index(x) < text.index(y)]
        uni: list[str] = [str(chr(0x0F0 + i)) for i in range(len(text))]
        for i in range(len(text)):
            func_str = func_str.replace(text[i], uni[i])
        dict_in = {uni[i]: all_vars[i] for i in range(len(text))}

        self._function = parse_expr(func_str, dict_in)
        self.data_errors = {e: None for e in self._errors_text}
        self.data_variables = {e: None for e in text}
        self.calculate_error_function()
        
        if not all(item in self._function.atoms(Symbol) for item in self._vars + self._consts) or len(self._function.atoms(Symbol)) != len(self._vars + self._consts):
            raise ValueError("The given variables and/or constants are not the same as in the given _function")
    
    def display_data(self):
        """
        Prints the function, constants and variables
        """
        print("Variables:")
        display(self._vars)
        print("Constants:")
        display(self._consts)
        print("Function:")
        display(self._function)
        if self._error_function != None:
            print("Error Function:")
            display(self._error_function)
    
    def calculate_error_function(self):
        """
        Calculates the error function of the function provided during class creation following the formula:

        Delta f(x1,...,xn) = sqrt((Delta x1 * df/dx1)^2 + ... + (Delta xn * df/dxn)^2)
        """
        if self._error_function:
            return self._error_function
        for i in range(len(self._vars)): 
            a = Mul(self._errors[i], diff(self._function, self._vars[i]), evaluate= False)
            b = Pow(a, 2, evaluate=False)
            self._error_function = Add(self._error_function, b)
        self._error_function = sqrt(self._error_function)
        
    def evaluate_function(self, subs: dict = {}):
        """
        Evaluates the function with the given values, which must be provided in the form of a Dictionary, for instance:

        let f(A,b,C,d) = (A*b)/(C*d) then to evaluate f at (0.5, 2, 3, -1) the input "subs" must be as follows:

        evaluate_function({"A": 0.5, "b": 2, "C": 3, "d": -1})

        Not all variables have to be supplied, for instance, for the above example the following input is valid:

        evaluate_function({"A": 0.5, "C": 3}) This will leave "b" and "d" as variables
        """
        if subs:
            if not all(item in self._consts_text + self._vars_text for item in subs.keys()):
                raise ValueError("The given variables and/or constants are not the same as in the given function")
            return float(self._function.evalf(subs=subs))
        
        subs = {e[0]: e[1] for e in self.data_variables.items() if e[1] != None}
        if any(isinstance(e, list) for e in subs.values()):
            list_keys = [e[0] for e in list(subs.items()) if isinstance(e[1], list)]
            n = len(subs[list_keys[0]])
            if not all(n == e for e in [len(subs[e]) for e in list_keys]):
                raise ValueError("'data' contains items which are lists of different length. All lists must be of equal length")
            res = []
            for i in range(n):
                cpy = subs.copy()
                for key in list_keys:
                    cpy[key] = subs[key][i]
                try:
                    res.append(float(self._function.evalf(subs=cpy)))
                except:
                    res.append(self._function.evalf(subs=cpy))
            return res
        else:
            try:
                return float(self._function.evalf(subs=subs))
            except:
                return self._function.evalf(subs=subs)
            
    
    def evaluate_error_function(self, subs: dict = {}):
        """
        Evaluates the error function with the given values, which must be provided in the form of a Dictionary, for instance:

        let Delta f(A,Delta A,B,Delta B) = sqrt((Delta A * B)^2 + (Delta B * A)^2) then to evaluate f at (0.5, 2, 3, -1) the input "subs" must be as follows:

        evaluate_function({"A": 0.5, "\\Delta A": 2, "C": 3, "\\Delta B": -1})

        Not all variables have to be supplied, for instance, for the above example the following input is valid:

        evaluate_function({"A": 0.5, "C": 3}) This will leave "\\Delta A" and "\\Delta B" as variables
        """
        if subs:
            if not all(item in self._consts_text + self._vars_text + self._errors_text for item in subs.keys()):
                raise ValueError("The given variables and/or constants are not the same as in the error function")
            return float(self._error_function.evalf(subs=subs))

        subs = {**self.data_variables, **self.data_errors} 
        subs = {e[0]: e[1] for e in subs.items() if e[1] != None}
        if any(isinstance(e, list) for e in subs.values()):
            list_keys = [e[0] for e in list(subs.items()) if isinstance(e[1], list)]
            n = len(subs[list_keys[0]])
            if not all(n == e for e in [len(subs[e]) for e in list_keys]):
                raise ValueError("'data' contains items which are lists of different length. All lists must be of equal length")
            res = []
            for i in range(n):
                cpy = subs.copy()
                for key in list_keys:
                    cpy[key] = subs[key][i]
                try:
                    res.append(float(self._error_function.evalf(subs=cpy)))
                except:
                    res.append(self._error_function.evalf(subs=cpy))
            return res
        else:
            try:
                return float(self._error_function.evalf(subs=subs))
            except:
                return self._error_function.evalf(subs=subs)

    def solve_function_for_variable(self, variable_to_solve: str, function_value = None, rest_of_variables: dict = None, symbolically = False):
        """
        Calculates the value the given variable "variable_to_solve" must have in order to make the error function equal "function_value"
        
        If "symbolically" is set to True, the only required input is "variable_to_solve"

        Useful for checking where the differences between experimental and theoretical values arise from, as it can give the value that the
        error must take in order to match the experimental value
        """
        if symbolically:
            function_value = Symbol("f")
            if variable_to_solve not in self._vars_text + self._consts_text:
                raise ValueError("value of variable_to_solve is not a parameter of error _function")
            return solve(Equality(self._function, function_value), Symbol(variable_to_solve))
        else:
            if rest_of_variables == None:
                if any(isinstance(e, list) for e in self.data_variables.values()):
                    raise ValueError("Some variable in data_variables is a list. Cannot work with lists")
                subs = {e[0]: e[1] for e in self.data_variables.items() if e[1] != None}
                subs.pop(variable_to_solve)
                return solve(Equality(self._function.evalf(subs=subs), function_value), Symbol(variable_to_solve))
            if not all(item in self._consts_text + self._vars_text + self._errors_text for item in rest_of_variables.keys()):
                raise ValueError("The given variables and/or constants are not the same as in the error _function")
            return solve(Equality(self._function.evalf(subs=rest_of_variables), function_value), Symbol(variable_to_solve))

    def solve_error_function_for_variable(self, variable_to_solve: str, function_value = None, rest_of_variables: dict = None, symbolically = False):
        """
        Calculates the value the given variable "variable_to_solve" must have in order to make the error function equal "function_value"
        
        If "symbolically" is set to True, the only required input is "variable_to_solve"

        Useful for checking where the differences between experimental and theoretical values arise from, as it can give the value that the
        error must take in order to match the experimental value
        """
        if symbolically:
            function_value = Symbol(self._error_mark + "f")
            if variable_to_solve not in self._vars_text + self._consts_text + self._errors_text:
                raise ValueError("value of variable_to_solve is not a parameter of error _function")
            return solve(Equality(self._error_function, function_value), Symbol(variable_to_solve))
        else:
            if rest_of_variables == None:
                subs = {**self.data_variables, **self.data_errors} 
                subs = {e[0]: e[1] for e in subs.items() if e[1] != None}
                subs.pop(variable_to_solve)
                if any(isinstance(e, list) for e in subs.values()):
                    raise ValueError("Some variable in data_variables is a list. Cannot work with lists")
                return solve(Equality(self._error_function.evalf(subs=subs), function_value), Symbol(variable_to_solve))
            if not all(item in self._consts_text + self._vars_text + self._errors_text for item in rest_of_variables.keys()):
                raise ValueError("The given variables and/or constants are not the same as in the error _function")
            return solve(Equality(self._error_function.evalf(subs=rest_of_variables), function_value), Symbol(variable_to_solve))
        
    def solve_error_function_for_all_variables(self, function_value = None, rest_of_variables: dict = None, symbolically: bool = False):
        """
        Solves the error function for each of the variables (x1, x2, ...) separately
        and returns either the required value for each variable in order to make the function == function_value
        (assuming the rest of the variables are as specified in rest_of_variables, ALL variables must be provided if a numerical result is desired)
        or the expression to get said result if "symbolically" is set to True
        """
        if symbolically:
            function_value = Symbol(self._error_mark + "f")
            for error in self._errors:
                print("---------------")
                display(error)
                print("=\n")
                display(solve(Equality(self._error_function, function_value), error))
                print("---------------")
        else:
            if rest_of_variables == None:
                subs = {**self.data_variables, **self.data_errors} 
                subs = {e[0]: e[1] for e in subs.items() if e[1] != None}
                dict_cpy = subs.copy()
                dict_cpy.pop(var.name)
                print("---------------")
                display(var)
                print("=\n")
                display(solve(Equality(self._error_function.evalf(subs=dict_cpy), function_value), var))
                print("---------------")
            if not all(item in self._consts_text + self._vars_text + self._errors_text for item in rest_of_variables.keys()):
                raise ValueError("The given variables and/or constants are not the same as in the error function")
            for var in self._vars:
                dict_cpy = rest_of_variables.copy()
                dict_cpy.pop(var.name)
                print("---------------")
                display(var)
                print("=\n")
                display(solve(Equality(self._error_function.evalf(subs=dict_cpy), function_value), var))
                print("---------------")


def error_function_from_sympy_expression(function, variables):
    error_function = 0
    errors = [r"\Delta " + e for e in variables]
    variables = [Symbol(e) for e in variables]
    errors = [Symbol(e) for e in errors]
    for i in range(len(variables)): 
        a = Mul(errors[i], diff(function, variables[i]), evaluate= False)
        b = Pow(a, 2, evaluate=False)
        error_function = Add(error_function, b)
    return sqrt(error_function)