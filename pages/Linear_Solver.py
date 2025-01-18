import streamlit as st
from models import LinearProgrammingSolver
import time
import io

operator_map = {
    "≤": "<=",
    "=": "==",
    "≥": ">="
}
# Usar CSS para modificar el tamaño del contenedor del gráfico
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1000px;  # Ajusta el ancho según lo desees
        }
    </style>
    """, unsafe_allow_html=True)

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
            new_restriction = {"lhs": lhs, "operator": operator, "rhs": str(rhs), "op_choice": operator_choice}
            if new_restriction in st.session_state["restrictions"]:
                st.warning("Esta restricción ya existe.")
            else:
                st.session_state["solver"].add_constraint(lhs, operator, rhs)
                st.session_state["restrictions"].append(new_restriction)
                st.success("Restricción agregada exitosamente.")
                st.rerun()
        else:
            st.error("El lado izquierdo no puede estar vacío.")
    
    # Botón para resolver el problema de programación lineal
    if st.button("Resolver Problema de Programación Lineal") and st.session_state["restrictions"]:
        # Resolver el problema
        st.session_state["solver"].solve()

        # Mostrar la solución
        st.subheader("Solución")
        
        if st.session_state["solver"].problem.status != 1:
            st.error("El problema no tiene solución óptima.")
        else:
            st.success("Problema resuelto exitosamente.")
        
            st.latex(r"\text{Valor Óptimo:}" + r"\quad " + str(st.session_state["solver"].problem.objective.value()))
            solution = st.session_state["solver"].get_solution()

            st.latex(r"\text{Solución:}" + r"\quad " + r",\quad ".join([f"{key} = {value}" for key, value in solution.items()]))

        
        # Testing de la region factible
        try:
            fig = st.session_state["solver"].plot_feasible_region()
            st.pyplot(fig=fig)
        
        except Exception as e:
            st.write(f"Nota: {e}")


# Columna lateral (col2): Eliminar restricciones
with col2:
    # Seccion Expandible para opciones
    with st.expander("Limites de Restricciones", expanded=False):
        low_bound = st.number_input("Límite Inferior", value=0)
        upper_bound = st.number_input("Límite Superior", value=10)
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
            st.session_state["solver"].remove_constraint(f"Restriccion_{selected_index}")
            st.rerun()
            st.success("Restricción eliminada.")
        
        # Botón para eliminar todas las restricciones
        if st.button("Eliminar todas", key="reset_restrictions"):
            st.session_state["restrictions"] = []
            for constraint_name in list(st.session_state["solver"].problem.constraints.keys()):
                del st.session_state["solver"].problem.constraints[constraint_name]
            st.success("Todas las restricciones han sido eliminadas.")
        
    
