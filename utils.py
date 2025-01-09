import inspect
import sympy as sp 
import re

def str_to_lambda(equation, reverse=False):
    """
    Convierte una cadena que describe una restricción en una función lambda.
    
    Parámetro:
    - equation: Una cadena con una expresión de restricción, como 'y >= 2'.
    
    Retorna:
    - Una función lambda que representa la restricción.
    """
    if not reverse:
        # Crear la expresión de la restricción a partir de la cadena
        return eval("lambda x, y: " + equation)
    else:
        text = inspect.getsource(equation).strip().split(":")[-1].strip()
        
        if text.endswith(","):
            text = text[:-1]
            
        return text
    

def parse_equation(equation_str):
    """
    Convierte una cadena de texto en formato 'ax + by operador c' a una ecuación o inecuación simbólica de SymPy.
    
    Parámetros:
    - equation_str: La ecuación o inecuación en formato de texto (por ejemplo: '2*x + 3*y <= 10').
    
    Retorna:
    - Una ecuación o inecuación simbólica que puede ser procesada por SymPy.
    """
    
    # Patrones para operadores y multiplicaciones explícitas
    pattern = r'^([\w\*\+\-\s]+)([<>=]=?|==)([\w\*\+\-\s]+)$'
    match = re.match(pattern, equation_str.strip())

    if not match:
        raise ValueError(f"La ecuación no tiene el formato correcto: {equation_str}")
    
    lhs_str, operator, rhs_str = match.groups()
    
    # Parsear el lado izquierdo (lhs) usando sympy.sympify
    lhs = sp.sympify(lhs_str.replace("^", "**"))
    rhs = sp.sympify(rhs_str)
    
    # Crear la ecuación o inecuación usando SymPy
    if operator == "=":
        return sp.Eq(lhs, rhs)
    elif operator == "<":
        return sp.LessThan(lhs, rhs)
    elif operator == ">":
        return sp.GreaterThan(lhs, rhs)
    elif operator == "<=":
        return sp.LessThan(lhs, rhs, strict=False)
    elif operator == ">=":
        return sp.GreaterThan(lhs, rhs, strict=False)
    
def format_to_sympy(equation_str):
    """
    Convierte una ecuación en formato textual como '4x + y <= 0'
    al formato compatible con SymPy como '4*x + y <= 0'.
    
    Parámetros:
    - equation_str: La ecuación o inecuación en formato de texto.
    
    Retorna:
    - Una cadena formateada para ser procesada por SymPy.
    """
    # Agregar el símbolo de multiplicación explícitamente entre números y variables
    equation_str = re.sub(r'(?<=\d)(?=[a-zA-Z])', '*', equation_str)

    # Asegurar que no haya espacios redundantes
    equation_str = re.sub(r'\s+', '', equation_str)
    
    # Reemplazar '^' por '**' para soportar exponentes en SymPy
    equation_str = equation_str.replace('^', '**')
    
    return equation_str

def extract_variables(objective_function):
    """
    Extrae las variables simbólicas de una función objetivo.

    Parámetro:
    - objective_function: Una cadena que representa la función objetivo.

    Retorna:
    - Un conjunto con las variables encontradas.
    """
    # Convertir la función objetivo en una expresión simbólica
    expr = sp.sympify(objective_function)

    # Extraer las variables simbólicas
    variables = expr.free_symbols

    return variables

def extract_coefficients(objective_function, variables):
    """
    Extrae los coeficientes de las variables en una función objetivo.
    
    Parámetros:
    - objective_function (str): La función objetivo como una cadena.
    - variables (list): Lista de variables (símbolos de SymPy) en la función objetivo.
    
    Retorna:
    - dict: Diccionario donde las claves son las variables y los valores son sus coeficientes.
    """
    # Convertir la función objetivo a una expresión de SymPy
    expr = sp.sympify(objective_function)
    
    # Extraer los coeficientes de cada variable
    coefficients = {var: expr.coeff(var) for var in variables}
    coeffs = coefficients.values()
    coeffs = [float(coeff) for coeff in coeffs]
    return coeffs