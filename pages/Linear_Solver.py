import streamlit as st
from models import LinearProgrammingSolver
from utils import OPERATOR_MAP, configure_page

def initialize_session_state():
    """Inicializa las variables de estado necesarias en la sesión."""
    if "objective" not in st.session_state:
        st.session_state["objective"] = ""
    if "restrictions" not in st.session_state:
        st.session_state["restrictions"] = []
    if "solver" not in st.session_state:
        st.session_state["solver"] = None

def handle_objective_function():
    """Gestión de la definición y actualización de la función objetivo."""
    st.subheader("Definir Función Objetivo")
    
    cols = st.columns([3, 1])
    with cols[0]:
        objective_input = st.text_input("Función Objetivo", value=st.session_state["objective"])
    with cols[1]:
        optimization_type = st.radio("Tipo", ["max", "min"])

    if objective_input != st.session_state["objective"] or \
       (st.session_state["solver"] and st.session_state["solver"].minimize != (optimization_type == "min")):

        st.session_state["objective"] = objective_input
        st.session_state["solver"] = LinearProgrammingSolver(minimize=(optimization_type == "min"))
        st.session_state["solver"].add_function(objective_input)
        st.session_state["solver"].set_objective()

    if st.session_state["objective"]:
        st.latex(f"{optimization_type}\\quad {st.session_state['objective']}")


def display_restrictions():
    """Muestra las restricciones actuales y permite agregarlas."""
    st.subheader("Restricciones Actuales")

    if st.session_state["restrictions"]:
        for i, restriction in enumerate(st.session_state["restrictions"], start=1):
            st.latex(f"{i}.\\quad {restriction['lhs']} {restriction['op_choice']} {restriction['rhs']}")
    else:
        st.write("No hay restricciones agregadas aún.")

    

def add_restrictions():
    st.subheader("Agregar Nueva Restricción")

    cols = st.columns([3, 1, 1, 2])
    with cols[0]:
        lhs = st.text_input("Lado Izquierdo", placeholder="Introduce la ecuación (ej. x + 2y)")
    with cols[1]:
        operator_choice = st.selectbox("Operador", ["≤", "=", "≥"])
    with cols[2]:
        rhs = st.number_input("Lado Derecho", value=0)

    with cols[3]:
        st.write(" ")
        st.write(" ")
        if st.button("Agregar Restricción"):
            if lhs.strip():
                new_restriction = {
                    "lhs": lhs,
                    "operator": OPERATOR_MAP[operator_choice],
                    "rhs": str(rhs),
                    "op_choice": operator_choice
                }
                
                if new_restriction in st.session_state["restrictions"]:
                    st.warning("Esta restricción ya existe.")
                else:
                    try:
                        st.session_state["solver"].add_constraint(lhs, OPERATOR_MAP[operator_choice], rhs)
                        st.session_state["restrictions"].append(new_restriction)
                        st.success("Restricción agregada exitosamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al agregar la restricción: Variable {e}")
                    
            else:
                st.error("El lado izquierdo no puede estar vacío.")


def solve_problem():
    """Resuelve el problema de programación lineal y muestra los resultados."""
    if st.button("Resolver Problema de Programación Lineal") and st.session_state["restrictions"]:
        solver = st.session_state["solver"]
        solver.solve()

        st.subheader("Solución")

        if solver.problem.status != 1:
            st.error("El problema no tiene solución óptima.")
        else:
            st.success("Problema resuelto exitosamente.")
            st.latex(r"\text{Valor Óptimo:} \quad " + str(solver.problem.objective.value()))
            solution = solver.get_solution()
            st.latex(r"\text{Solución:} \quad " + ",\quad ".join([f"{key} = {value}" for key, value in solution.items()]))

            try:
                fig = solver.plot_feasible_region()
                st.pyplot(fig=fig)
            except Exception as e:
                st.write(f"Nota: {e}")

def manage_restrictions():
    """Gestión de la eliminación de restricciones."""
    with st.expander("Eliminar Restricciones", expanded=False):
        if not st.session_state["restrictions"]:
            st.write("No hay restricciones para eliminar.")
            return

        selected_index = st.selectbox(
            "Selecciona la restricción:",
            options=range(len(st.session_state["restrictions"])),
            format_func=lambda i: f"{i + 1}. {st.session_state['restrictions'][i]['lhs']} {st.session_state['restrictions'][i]['op_choice']} {st.session_state['restrictions'][i]['rhs']}"
        )

        if st.button("Eliminar"):
            del st.session_state["restrictions"][selected_index]
            st.session_state["solver"].remove_constraint(f"Restriccion_{selected_index}")
            st.rerun()

        if st.button("Eliminar todas", key="reset_restrictions"):
            st.session_state["restrictions"] = []
            st.session_state["solver"].clear_constraints()
            st.success("Todas las restricciones han sido eliminadas.")
            st.rerun()

# Configuración inicial
configure_page()
initialize_session_state()

# Título de la aplicación
st.title("Solver de restricciones lineales")

# Layout principal
col1, col2 = st.columns([3, 1])

with col1:
    handle_objective_function()
    display_restrictions()
    add_restrictions()
    solve_problem()

with col2:
    manage_restrictions()
