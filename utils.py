import inspect
import sympy as sp 
import re
import numpy as np
import matplotlib.pyplot as plt

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
    

import re
import sympy as sp

def parse_equation(equation_str):
    """
    Convierte una cadena de texto en formato 'ax + by operador c' a una ecuación o inecuación simbólica de SymPy.
    
    Parámetros:
    - equation_str: La ecuación o inecuación en formato de texto (por ejemplo: '2*x + 3*y <= 10').
    
    Retorna:
    - Una ecuación o inecuación simbólica que puede ser procesada por SymPy.
    """
    # Patrón para separar lhs, operador y rhs
    pattern = r'^(.*?)\s*(<=|>=|<|>|==|=)\s*(.*?)$'
    match = re.match(pattern, equation_str.strip())

    if not match:
        raise ValueError(f"La ecuación no tiene el formato correcto: {equation_str}")
    
    # Extraer partes: lado izquierdo, operador, lado derecho
    lhs_str, operator, rhs_str = match.groups()

    # Normalizar el operador '=' a '=='
    if operator == "=":
        operator = "=="

    # Normalizar y verificar lhs y rhs
    lhs_str = lhs_str.strip()
    rhs_str = rhs_str.strip()
    if not lhs_str:
        raise ValueError(f"El lado izquierdo (lhs) está vacío: {equation_str}")
    if not rhs_str:
        raise ValueError(f"El lado derecho (rhs) está vacío: {equation_str}")

    try:
        # Parsear lhs y rhs usando sympy.sympify
        lhs = sp.sympify(lhs_str.replace("^", "**"))
        rhs = sp.sympify(rhs_str)
    except sp.SympifyError as e:
        raise ValueError(f"Error al interpretar la ecuación: {equation_str}") from e

    # Crear la ecuación o inecuación usando SymPy
    if operator == "==":
        return sp.Eq(lhs, rhs)
    elif operator == "<":
        return sp.LessThan(lhs, rhs, strict=True)
    elif operator == ">":
        return sp.GreaterThan(lhs, rhs, strict=True)
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


def get_range(constraints, variable):
    """
    Obtiene un rango aproximado para una variable ('x' o 'y') evaluando las restricciones en un conjunto de puntos.
    
    Parámetros:
    - constraints: Lista de funciones lambda que representan las restricciones.
    - variable: La variable para la cual se quiere calcular el rango ('x' o 'y').
    
    Retorna:
    - Un rango aproximado (min, max) para la variable especificada.
    """
    y_max = set()
    y_min = set()
    x_max = set()
    x_min = set()

    # Graficar las líneas de las restricciones
    for constraint in constraints:
        # Resolver la restricción para y
        eq = str_to_lambda(constraint, reverse=True)  # Asumimos que puedes convertir la función lambda a string
        eq = format_to_sympy(eq)
        eq = parse_equation(eq)
        eq = sp.Eq(eq.lhs, eq.rhs)
        
        # Resolvemos la ecuación para 'y' si se puede
        try:
            eq_y = sp.Eq(eq.lhs, eq.rhs)
            solution_for_y = sp.solve(eq_y, "y")
            if solution_for_y:  
                y_max.add(max([solution_for_y[0].subs("x", i) for i in range(-10, 11)])) 
                y_min.add(min([solution_for_y[0].subs("x", i) for i in range(-10, 11)])) 
        except Exception as e:
            print(f"No se puede resolver para y: {e}")
        
        # Resolvemos la ecuación para 'x' si se puede
        try:
            eq_x = sp.Eq(eq.lhs, eq.rhs)
            solution_for_x = sp.solve(eq_x, "x")
            if solution_for_x:  # Si se puede resolver para 'x'
                x_max.add(max([solution_for_x[0].subs("y", i) for i in range(-10, 11)]))
                x_min.add(min([solution_for_x[0].subs("y", i) for i in range(-10, 11)]))
        except Exception as e:
            print(f"No se puede resolver para x: {e}")
        
    if variable == "x":
        return min(x_min), max(x_max)
    else:
        return min(y_min), max(y_max)



def plot_feasible_region_and_constraints(lambda_constraints, str_constraints, x_range=(0, 16), y_range=(0, 11), resolution=300):
    """
    Grafica la región factible y las restricciones para un problema de programación lineal.
    
    Parámetros:
    - lambda_constraints: Lista de funciones de restricciones, cada una en forma de una lambda.
    - str_constraints: Lista de restricciones en formato de texto.
    - x_range: Rango para el eje x.
    - y_range: Rango para el eje y.
    - resolution: Resolución de la cuadrícula para calcular la región factible.
    
    Retorna:
    - fig: Objeto Figure de Matplotlib.
    """
    # Usar estilo de fondo oscuro
    plt.style.use('dark_background')

    # Crear el espacio de valores de x y y
    d = np.linspace(x_range[0], x_range[1], resolution)
    x, y = np.meshgrid(d, d)
    
    # Crear figura y ejes
    fig, ax = plt.subplots()
    
    # Graficar la región factible
    feasible_region = np.ones_like(x, dtype=bool)
    for constraint in lambda_constraints:
        feasible_region &= constraint(x, y)
    
    ax.imshow(feasible_region.astype(int), extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="inferno", alpha=0.5)
    
    # Graficar las líneas de las restricciones
    for constraint in str_constraints:
        # Resolver la restricción para y
        eq = format_to_sympy(constraint)
        eq = parse_equation(eq)
        eq = sp.Eq(eq.lhs, eq.rhs)
        
        # Resolvemos la ecuación para 'y' si se puede
        try:
            eq_y = sp.Eq(eq.lhs, eq.rhs)
            solution_for_y = sp.solve(eq_y, "y")
            if solution_for_y:  # Si se puede resolver para 'y'
                y_vals = [solution_for_y[0].subs("x", i) for i in x[0]]
                ax.plot(x[0], y_vals, label=str(constraint))
                continue
        except Exception as e:
            print(f"No se puede resolver para y: {e}")
        
        # Resolvemos la ecuación para 'x' si se puede
        try:
            eq_x = sp.Eq(eq.lhs, eq.rhs)
            solution_for_x = sp.solve(eq_x, "x")
            if solution_for_x:  # Si se puede resolver para 'x'
                x_vals = [solution_for_x[0].subs("y", i) for i in y[:, 0]]  # Usamos y[:, 0] para obtener valores de y
                ax.plot(x_vals, y[:, 0], label=str(constraint))
                continue
        except Exception as e:
            print(f"No se puede resolver para x: {e}")
    
    # Configuración del gráfico
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.grid(True)
    ax.legend() 
    
    return fig


