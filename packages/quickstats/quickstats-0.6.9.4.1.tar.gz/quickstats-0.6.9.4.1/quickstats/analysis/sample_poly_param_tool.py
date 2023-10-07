from typing import List, Dict, Optional, Union

from quickstats import AbstractObject, semistaticmethod

from quickstats.maths.numerics import to_rounded_float, str_encode_value
from quickstats.utils.common_utils import in_notebook

class SamplePolyParamTool(AbstractObject):
    
    def __init__(self, verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)
        
    def initialize_symbols(self, parameters:List[str], coefficients:List[str],
                           bases:List[str], latex_map:Optional[Dict]=None):
        if latex_map is None:
            latex_map = {}
        from sympy import Symbol
        parameter_symbols = {}
        coefficient_symbols = {}
        basis_symbols = {}
        for parameter in parameters:
            parameter_symbols[parameter] = Symbol(latex_map.get(parameter, parameter))
        for coefficient in coefficients:
            coefficient_symbols[coefficient] = Symbol(latex_map.get(coefficient, coefficient))
        basis_symbols = {}
        for basis in bases:
            basis_symbols[basis] = Symbol(basis)
        return parameter_symbols, coefficient_symbols, basis_symbols
    
    @semistaticmethod
    def initialize_formula(self, formula_str:str, parameters:Dict, coefficients:Dict,
                           latex_map:Optional[Dict]=None):
        from sympy import simplify
        formula = simplify(formula_str)
        if latex_map is None:
            return formula
        symbols = list(formula.free_symbols)
        subs = []
        for symbol in symbols:
            is_parameter, is_coefficient = False, False
            name = symbol.name
            if name in parameters:
                is_parameter = True
            if name in coefficients:
                is_coefficient = True
            if is_parameter and is_coefficient:
                raise ValueError(f'variable "{name}" in the formula "{formula_str}" can not be both '
                                 'a parameter and a coefficient')
            elif (not is_parameter) and (not is_coefficient):
                raise ValueError(f'variable "{name}" in the formula "{formula_str}" is neither a '
                                 'parameter or a coefficient')
            elif is_parameter and (name in latex_map):
                subs.append([symbol, parameters[name]])
            elif is_coefficient and (name in latex_map):
                subs.append([symbol, coefficients[name]])
        formula = formula.subs(subs)
        return formula                
    
    def get_basis_symbol_names(self, basis_values:List[Dict], parameters:List[str],
                               latex_map:Optional[Dict]=None):
        if latex_map is None:
            latex_map = {}
        symbol_names = []
        for values in basis_values:
            components = []
            for parameter in parameters:
                value = to_rounded_float(values[parameter])
                component = f"{latex_map.get(parameter, parameter)}={value}"
                components.append(component)
            symbol_name = f"Yield({','.join(components)})"
            symbol_names.append(symbol_name)
        return symbol_names
    
    def display_expression(self, expr):
        if not in_notebook():
            self.stdout.info(str(expr), bare=True)
        else:
            from IPython import display
            display.display(expr)
            
    def display_sets(self, *objects):
        from sympy import FiniteSet
        self.display_expression(FiniteSet(*objects))
        
    def display_equation(self, variable, expression):
        from sympy import Eq
        self.display_expression(Eq(variable, expression))
    
    def solve_coefficients(self, formula, parameter_symbols:Dict, coefficient_symbols:Dict,
                    basis_symbols:Dict, basis_value_map:Dict):
        from sympy import simplify, solve
        equations = []
        for basis_name, basis_values in basis_value_map.items():
            subs = [(parameter_symbols[k], simplify(v)) for k, v in basis_values.items()]
            equation_i = formula.subs(subs) - basis_symbols[basis_name]
            equations.append(equation_i)
        solutions = solve(equations, list(coefficient_symbols.values()), dict=True)
        return solutions
    
    def _get_inverse_latex_map(self, latex_map:Dict):
        return {v:k for k,v in latex_map.items()}
    
    def get_delatexed_formula(self, formula, inverse_latex_map:Dict):
        symbols = list(formula.free_symbols)
        subs = []
        for symbol in symbols:
            name = symbol.name
            if name in inverse_latex_map:
                subs.append([symbol, inverse_latex_map[name]])
        formula = formula.subs(subs)
        return formula
    
    def run_linear_combination(self, formula:str, parameters:List[str], coefficients:List[str],
                               basis_samples:Dict[str, Dict], latex_map:Optional[Dict]=None):
        if len(coefficients) != len(basis_samples):
            raise ValueError("number of basis samples must equal the number of coefficients in the polynomial")
        param_data = {}
        param_data['sample'] = []
        param_data['expression'] = []
        for parameter in parameters:
            param_data[parameter] = []
        samples = list(basis_samples.keys())
        basis_values = list(basis_samples.values())
        bases = self.get_basis_symbol_names(basis_values, parameters, latex_map=latex_map)
        parameter_symbols, coefficient_symbols, basis_symbols = self.initialize_symbols(parameters,
                                                                                        coefficients,
                                                                                        bases,
                                                                                        latex_map=latex_map)
        basis_value_map = dict(zip(bases, basis_values))
        basis_sample_map = dict(zip(bases, samples))
        formula_expr = self.initialize_formula(formula, parameter_symbols,
                                               coefficient_symbols, latex_map=latex_map)
        self.stdout.info("Formula:", bare=True)
        self.display_expression(formula_expr)
        self.stdout.info("Parameters:", bare=True)
        self.display_sets(*parameter_symbols.values())
        self.stdout.info("Coefficients:", bare=True)
        self.display_sets(*coefficient_symbols.values())
        solutions = self.solve_coefficients(formula_expr, parameter_symbols, coefficient_symbols,
                                            basis_symbols, basis_value_map)
        if len(solutions) == 0:
            raise RuntimeError("unable to solve the system of linear equations")
        elif len(solutions) > 1:
            raise RuntimeError("system of linear equations gives non-unique solutions")
        solution = solutions[0]
        self.stdout.info("Solutions:", bare=True)
        for coefficient in coefficient_symbols.values():
            self.display_equation(coefficient, solution[coefficient])
        subs = [(k, v) for k, v in solution.items()]
        resolved_formula = formula_expr.subs(subs).expand()
        coefficient_map = {basis:resolved_formula.coeff(basis_symbols[basis]) for basis in bases}
        inverse_latex_map = self._get_inverse_latex_map(latex_map)
        coefficient_map_delatexed = {}
        for basis, coefficient_formula in coefficient_map.items():
            coefficient_map_delatexed[basis] = self.get_delatexed_formula(coefficient_formula, inverse_latex_map)
        self.stdout.info("Contribution from basis sample:", bare=True)
        for basis, expr in coefficient_map.items():
            self.display_equation(basis_symbols[basis], expr)
        for basis in bases:
            param_data['sample'].append(basis_sample_map[basis])
            for parameter, value in basis_value_map[basis].items():
                param_data[parameter].append(to_rounded_float(value))
            basis_symbol = basis_symbols[basis]
            param_data['expression'].append(str(coefficient_map_delatexed[basis]))
        return param_data
        
    def run_parameterization(self, formula:str, parameters:List[str], coefficients:List[str],
                             basis_samples:Dict[str, Dict], method:str='linear_combination',
                             latex_map:Optional[Dict]=None, saveas:Optional[str]=None):
        if method == 'linear_combination':
            result = self.run_linear_combination(formula, parameters, coefficients, basis_samples,
                                                 latex_map=latex_map)
        else:
            raise ValueError(f"unsupported method: {method}")
        if saveas is not None:
            with open(saveas, 'w') as file:
                json.dump(result, saveas, indent=2)
        return result