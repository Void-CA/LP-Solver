from pulp import LpProblem, LpVariable, LpMinimize, lpSum
import utils
class LinearProgrammingSolver:
    def __init__(self, problem_name="LP_Problem", minimize=True):
        self.problem = LpProblem(problem_name, LpMinimize if minimize else -1)
        self.variables = {}
        self.constraints = []

    def add_function(self, objective_function, low_bound=0, up_bound=None, cat="Continuous"):
        """
        Agrega variables de decisión basadas en las variables extraídas de una función objetivo.
        
        Parámetros:
        - objective_function: Cadena que representa la función objetivo.
        - low_bound: Límite inferior para las variables (por defecto 0).
        - up_bound: Límite superior para las variables (por defecto None).
        - cat: Tipo de variable (por defecto 'Continuous').

        Retorna:
        - Un diccionario con las variables creadas.
        """
        # Extraer variables de la función objetivo
        self.objective_function = objective_function
        variables = utils.extract_variables(objective_function)
        
        # Crear las variables de decisión
        for var in variables:
            var_name = str(var)  # Convertir el identificador simbólico en un nombre
            self.variables[var_name] = LpVariable(var_name, lowBound=low_bound, upBound=up_bound, cat=cat)
        
        return self.variables

    def set_objective(self):
        """Define la función objetivo."""
        objective_expr = utils.parse_equation(self.objective_function)
        objective_terms = [objective_expr.subs(var, self.variables[var_name]) for var_name, var in self.variables.items()]
        self.problem += lpSum(objective_terms), "Objective"

    def add_constraint(self, constraint, name):
        """Agrega una restricción al problema."""
        self.problem += constraint, name

    def solve(self):
        """Resuelve el problema y retorna el estado."""
        self.problem.solve()
        return self.problem.status, self.problem.objective.value()

    def get_solution(self):
        """Retorna los valores de las variables de decisión."""
        return {name: var.varValue for name, var in self.variables.items()}
    

class ResourceAssignmentSolver:
    def __init__(self, cost_matrix, max_resources_per_task=1, max_tasks_per_resource=1, allow_unassigned_tasks=False, variable_type="Binary"):
        if any(len(row) != len(cost_matrix[0]) for row in cost_matrix):
            raise ValueError("cost_matrix debe ser una matriz rectangular.")
        
        self.cost_matrix = cost_matrix
        self.max_resources_per_task = max_resources_per_task
        self.max_tasks_per_resource = max_tasks_per_resource
        self.allow_unassigned_tasks = allow_unassigned_tasks
        self.variable_type = variable_type

        self.problem = LpProblem("Resource_Assignment", LpMinimize)
        self.num_tasks = len(cost_matrix[0])
        self.num_resources = len(cost_matrix)
        self.x = [[LpVariable(f"x_{i}_{j}", cat=self.variable_type) for j in range(self.num_tasks)] for i in range(self.num_resources)]
    
    def add_resource(self, default_cost=1e6):
        self.cost_matrix.append([default_cost] * self.num_tasks)
        self.x.append([LpVariable(f"x_{self.num_resources}_{j}", cat=self.variable_type) for j in range(self.num_tasks)])
        self.num_resources += 1
    
    def add_task(self, default_cost=1e6):
        for row in self.cost_matrix:
            row.append(default_cost)
        for i in range(self.num_resources):
            self.x[i].append(LpVariable(f"x_{i}_{self.num_tasks}", cat=self.variable_type))
        self.num_tasks += 1
    
    def set_objective(self):
        self.problem += lpSum(self.cost_matrix[i][j] * self.x[i][j] for i in range(self.num_resources) for j in range(self.num_tasks)), "Costo_Total"
    
    def add_constraints(self):
        for j in range(self.num_tasks):
            self.problem += lpSum(self.x[i][j] for i in range(self.num_resources)) == self.max_resources_per_task, f"Tarea_{j}_asignada"
        for i in range(self.num_resources):
            self.problem += lpSum(self.x[i][j] for j in range(self.num_tasks)) <= self.max_tasks_per_resource, f"Recurso_{i}_limite_tareas"
        if self.allow_unassigned_tasks:
            for j in range(self.num_tasks):
                self.problem += lpSum(self.x[i][j] for i in range(self.num_resources)) <= 1, f"Tarea_{j}_opcional"

    def solve(self):
        self.set_objective()
        self.add_constraints()
        self.problem.solve()
        if self.problem.status != 1:
            raise Exception(f"Problema no factible o sin solución. Estado: {self.problem.status}")
        return self.problem.status, self.problem.objective.value()
    
    def get_solution(self):
        return {(i, j): self.x[i][j].varValue for i in range(self.num_resources) for j in range(self.num_tasks) if self.x[i][j].varValue > 0}


        
