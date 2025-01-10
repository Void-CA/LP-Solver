import streamlit as st
import sympy as sp
from models import LinearProgrammingSolver

operator_map = {
    "≤": "<=",
    "=": "=",
    "≥": ">="
}

# Título de la aplicación
st.title("Gestión de Restricciones")

# Crear 2 columnas: una para la parte principal y otra para el panel lateral (eliminar restricciones)
col1, col2 = st.columns([3, 1])  # 3 partes para el contenido principal y 1 parte para el panel lateral

# Columna principal (col1): Agregar y Mostrar restricciones
with col1:
    typeof_optimization = "max"
    if "objective" not in st.session_state:
        st.session_state["objective"] = ""
    
    objective_column, type_column = st.columns([5, 1])

    with objective_column:
        st.subheader("Definir Función Objetivo")
        st.session_state["objective"] = st.text_input("Función Objetivo", value=st.session_state["objective"])

    with type_column:
        st.subheader("")
        typeof_optimization = st.radio("Tipo", ["max", "min"])



    # Configurar el objetivo si está definido
    if st.session_state["objective"]:

        if "solver" not in st.session_state:
            st.session_state["solver"] = LinearProgrammingSolver(minimize=typeof_optimization == "min")
            st.session_state["solver"].add_function(st.session_state["objective"])
            st.session_state["solver"].set_objective()

        objective_has_changed = (
            st.session_state["solver"].objective != st.session_state["objective"] or 
            st.session_state["solver"].minimize != (typeof_optimization == "min")
            )

        if objective_has_changed:
            print("Cambiando el Solver")
            st.session_state["solver"] = LinearProgrammingSolver(minimize=typeof_optimization == "min")
            st.session_state["solver"].add_function(st.session_state["objective"])
            st.session_state["solver"].set_objective()

        st.latex(f"{typeof_optimization}\\quad {st.session_state['objective']}")


    # Espacio para almacenar restricciones
    if "restrictions" not in st.session_state:
        st.session_state["restrictions"] = []

    # Mostrar restricciones actuales
    st.subheader("Restricciones Actuales")
    if st.session_state["restrictions"]:
        for i, r in enumerate(st.session_state["restrictions"], start=1):
            latex_equation = f"{i}.\\quad {r['lhs']} {r['op_choice']} {r['rhs']}"
            st.latex(latex_equation)
    else:
        st.write("No hay restricciones agregadas aún.")

    # Agregar nueva restricción
    st.subheader("Agregar Nueva Restricción")

    # Dividir los inputs en columnas
    lhs_col, operator_col, rhs_col = st.columns([3, 1, 1])  # Anchos proporcionales: 3-1-1

    # Inputs en columnas
    with lhs_col:
        lhs = st.text_input("Lado Izquierdo", placeholder="Introduce la ecuación (ej. x + 2y)")
    with operator_col:
        operator_choice = st.selectbox("Operador", ["≤", "=", "≥"])
        operator = operator_map[operator_choice]
    with rhs_col:
        rhs = st.number_input("Lado Derecho", value=0)


    # Botón para agregar la restricción
    if st.button("Agregar Restricción"):
        if lhs.strip():  # Verifica que el LHS no esté vacío
            new_restriction = {"lhs": lhs, "operator": operator, "rhs": rhs, "op_choice": operator_choice}
            if new_restriction in st.session_state["restrictions"]:
                st.warning("Esta restricción ya existe.")
            else:
                st.session_state["solver"].add_constraint(lhs, operator, str(rhs), f"restriccion_{len(st.session_state['restrictions'])}")
                st.session_state["restrictions"].append(new_restriction)
                st.success("Restricción agregada exitosamente.")
                print(st.session_state["solver"])
                print(st.session_state["solver"].problem)
        else:
            st.error("El lado izquierdo no puede estar vacío.")
    
    # Botón para resolver el problema de programación lineal
    if st.button("Resolver Problema de Programación Lineal") and st.session_state["restrictions"]:
        # Resolver el problema
        st.session_state["solver"].solve()

        # Mostrar la solución
        st.subheader("Solución")
        st.write("Estado:", st.session_state["solver"].problem.status)
        st.write("Valor Óptimo:", st.session_state["solver"].problem.objective.value())
        st.latex(st.session_state["solver"].get_solution())

# Columna lateral (col2): Eliminar restricciones
with col2:
    # Sección Expandible para Eliminar Restricciones
    with st.expander("Eliminar Restricciones", expanded=False):
        if not st.session_state["restrictions"]:

            st.write("No hay restricciones para eliminar.")
            
        
        # Crear un menú desplegable con las restricciones numeradas
        selected_index = st.selectbox(
            "Selecciona la restricción:",
            options=range(len(st.session_state["restrictions"])),
            format_func=lambda i: f"{i + 1}. {st.session_state['restrictions'][i]['lhs']} {st.session_state['restrictions'][i]['operator']} {st.session_state['restrictions'][i]['rhs']}"
        )
        # Botón para eliminar la restricción seleccionada
        if st.button("Eliminar"):
            del st.session_state["restrictions"][selected_index]
            del st.session_state["solver"].problem.constraints[f"restriccion_{selected_index}"]
            st.success("Restricción eliminada.")
        
        if st.button("Resetear"):
            st.session_state["restrictions"] = []
            for constraint_name in list(st.session_state["solver"].problem.constraints.keys()):
                del st.session_state["solver"].constraints[constraint_name]
            st.success("Todas las restricciones han sido eliminadas.")
        
    
