import streamlit as st
import pandas as pd
from models import ResourceAssignmentSolver
from st_aggrid import AgGrid, GridOptionsBuilder
from utils import configure_page

# Configuración inicial
def setup_page():
    configure_page()
    st.title("Solver de Asignación de Recursos")
    st.warning("Este módulo está en desarrollo y puede no funcionar correctamente.")

# Opciones avanzadas
def advanced_options():
    if "advanced_settings" not in st.session_state:
        st.session_state.advanced_settings = {
            "max_resources_per_task": 1,
            "max_tasks_per_resource": 1,
            "variable_type": "Binaria",
            "allow_unassigned_tasks": False,
        }

    col_options = st.columns(3)
    with col_options[0]:
        st.session_state.advanced_settings["max_resources_per_task"] = st.number_input(
            "Máximo de recursos por tarea", 
            min_value=1, 
            step=1, 
            value=st.session_state.advanced_settings["max_resources_per_task"]
        )
    with col_options[1]:
        st.session_state.advanced_settings["max_tasks_per_resource"] = st.number_input(
            "Máximo de tareas por recurso", 
            min_value=1, 
            step=1, 
            value=st.session_state.advanced_settings["max_tasks_per_resource"]
        )
    with col_options[2]:
        st.session_state.advanced_settings["variable_type"] = st.selectbox(
            "Tipo de variable", 
            ["Binaria", "Continua", "Entera"], 
            index=["Binaria", "Continua", "Entera"].index(st.session_state.advanced_settings["variable_type"])
        )
    st.session_state.advanced_settings["allow_unassigned_tasks"] = st.checkbox(
        "Permitir tareas no asignadas", 
        value=st.session_state.advanced_settings["allow_unassigned_tasks"]
    )


# Creación y edición de matriz
def create_and_edit_matrix(num_resources, num_workers):
    matrix = pd.DataFrame(
        [[0 for _ in range(num_workers)] for _ in range(num_resources)],
        columns=[f"Trabajador {i+1}" for i in range(num_workers)],
        index=[f"Recurso {i+1}" for i in range(num_resources)]
    )
    matrix.insert(0, "Recurso", matrix.index)
    gb = GridOptionsBuilder.from_dataframe(matrix)
    gb.configure_default_column(editable=True)
    gb.configure_column("Recurso", editable=False)
    grid_options = gb.build()
    response = AgGrid(matrix, gridOptions=grid_options, editable=True, fit_columns_on_grid_load=True)
    return response

# Procesar datos
def process_data(data):
    solver = ResourceAssignmentSolver(
        data
    )
    print(solver)
    solver.solve()
    assignments = solver.get_assignment()
    assignments_df = pd.DataFrame(assignments.items(), columns=["Recurso", "Trabajador"]).sort_values("Recurso")
    return assignments_df

# Opción: Imputar manualmente
def manual_input():
    st.subheader("Ingresar datos manualmente")
    cols = st.columns(2)
    with cols[0]:
        num_resources = st.number_input("Cantidad de recursos", min_value=1, step=1, value=3)
    with cols[1]:
        num_workers = st.number_input("Cantidad de trabajadores", min_value=1, step=1, value=3)

    with st.expander("**Opciones avanzadas**"):
        advanced_options()

    response = create_and_edit_matrix(int(num_resources), int(num_workers))
    if st.button("Procesar datos manuales"):
        updated_matrix = pd.DataFrame(response["data"])
        dcols = st.columns(2)
        with dcols[0]:
            st.write("Datos ingresados:")
            st.dataframe(updated_matrix)
        with dcols[1]:
            solution = process_data(updated_matrix)
            st.write("Resultado:")
            st.dataframe(solution)

# Opción: Cargar desde CSV
def load_csv():
    st.subheader("Subir archivo CSV")
    with st.expander("**Opciones avanzadas**"):
        advanced_options()
    uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.subheader("Editar datos del CSV")
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_default_column(editable=True)
        grid_options = gb.build()
        response = AgGrid(data, gridOptions=grid_options, editable=True, fit_columns_on_grid_load=True)
        if st.button("Procesar datos del CSV"):
            edited_data = pd.DataFrame(response["data"])
            st.write("Datos originales:")
            st.dataframe(data)
            st.write("Datos editados:")
            st.dataframe(edited_data)

# Descargar datos procesados
def download_data(response, input_option):
    if st.button("Descargar datos procesados"):
        if input_option == "Imputar manualmente" and 'response' in locals():
            data_to_download = pd.DataFrame(response["data"])
        elif input_option == "Cargar desde CSV" and 'response' in locals():
            data_to_download = pd.DataFrame(response["data"])
        else:
            data_to_download = None

        if data_to_download is not None:
            csv = data_to_download.to_csv(index=False).encode("utf-8")
            st.download_button("Descargar CSV", data=csv, file_name="datos_procesados.csv", mime="text/csv")
        else:
            st.warning("No hay datos procesados para descargar.")

# Main
def main():
    setup_page()
    input_option = st.radio("Selecciona cómo ingresar los datos:", ("Imputar manualmente", "Cargar desde CSV"), horizontal=True)
    if input_option == "Imputar manualmente":
        manual_input()
    elif input_option == "Cargar desde CSV":
        load_csv()

if __name__ == "__main__":
    main()
