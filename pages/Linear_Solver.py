import streamlit as st
import sympy as sp
from models import LinearProgrammingSolver



# Título de la aplicación
st.title("Gestión de Restricciones")

# Crear 2 columnas: una para la parte principal y otra para el panel lateral (eliminar restricciones)
col1, col2 = st.columns([3, 1])  # 3 partes para el contenido principal y 1 parte para el panel lateral

# Columna principal (col1): Agregar y Mostrar restricciones
with col1:
    if "objective" not in st.session_state:
        st.session_state["objective"] = ""
    
    objective_column, type_column = st.columns([5, 1])

    with objective_column:
        st.subheader("Definir Función Objetivo")
        st.session_state["objective"] = st.text_input("Función Objetivo", value=st.session_state["objective"])

    with type_column:
        st.subheader("")
        typeof_optimization = st.radio("Tipo", ["max", "min"])
    
    if st.session_state["objective"]:
            st.latex(f"{typeof_optimization}\\quad {st.session_state["objective"]}")
    solver = LinearProgrammingSolver(minimize=(typeof_optimization == "min"))
    
    # Espacio para almacenar restricciones
    if "restrictions" not in st.session_state:
        st.session_state["restrictions"] = []

    # Mostrar restricciones actuales
    st.subheader("Restricciones Actuales")
    if st.session_state["restrictions"]:
        for i, r in enumerate(st.session_state["restrictions"], start=1):
            latex_equation = f"{i}.\\quad {r['lhs']} {r['operator']} {r['rhs']}"
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
        operator = st.selectbox("Operador", ["≤", "=", "≥"])
    with rhs_col:
        rhs = st.number_input("Lado Derecho", value=0.0)

    # Botón para agregar la restricción
    if st.button("Agregar Restricción"):
        if lhs.strip():  # Verifica que el LHS no esté vacío
            # Agregar la nueva restricción al estado
            st.session_state["restrictions"].append({
                "lhs": lhs,
                "operator": operator,
                "rhs": rhs
            })
            # Mensaje de éxito
            st.success("Restricción agregada exitosamente.")
            st.rerun()
        else:
            st.error("El lado izquierdo no puede estar vacío.")
    
    # Botón para resolver el problema de programación lineal
    if st.button("Resolver Problema de Programación Lineal"):
        if st.session_state["restrictions"]:
            # Resolver el problema de programación lineal
            solver.set_restrictions(st.session_state["restrictions"])
            solver.solve()
            # Mostrar la solución
            st.subheader("Solución")
            st.latex(solver.get_solution())
        else:
            st.error("Agrega al menos una restricción para resolver el problema de programación lineal.")

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
            st.success("Restricción eliminada.")
            st.rerun()
        
    
