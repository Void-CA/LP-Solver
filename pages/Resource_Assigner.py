import streamlit as st
import pandas as pd
from models import ResourceAssignmentSolver
from st_aggrid import AgGrid, GridOptionsBuilder

# Use CSS to modify the container size
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1000px;
        }
    </style>
    """, unsafe_allow_html=True)

def app():

    st.title("Solver de Asignación de Recursos")

    # Option: Input data manually or load from CSV
    input_option = st.radio("Selecciona cómo ingresar los datos:", ("Imputar manualmente", "Cargar desde CSV"), horizontal=True)

    if input_option == "Imputar manualmente":

        # Request table dimensions
        dimensions_cols = st.columns(2)
        with dimensions_cols[0]:
            num_resources = st.number_input("Cantidad de recursos", min_value=1, step=1, value=3)
        with dimensions_cols[1]:
            num_workers = st.number_input("Cantidad de trabajadores", min_value=1, step=1, value=3)

        with st.expander("Opciones avanzadas"):
            col_options = st.columns(3)
            with col_options[0]:
                max_resources_per_task = st.number_input("Máximo de recursos por tarea", min_value=1, step=1, value=1)
            with col_options[1]:
                max_tasks_per_resource = st.number_input("Máximo de tareas por recurso", min_value=1, step=1, value=1)
            with col_options[2]:
                variable_type = st.selectbox("Tipo de variable", ["Binaria", "Continua"], index=0)

            allow_unassigned_tasks = st.checkbox("Permitir tareas no asignadas", value=False)


        # Create an initial empty DataFrame
        if num_resources > 0 and num_workers > 0:
            matrix = pd.DataFrame(
                [[0 for _ in range(int(num_workers))] for _ in range(int(num_resources))],
                columns=[f"Trabajador {i+1}" for i in range(int(num_workers))],
                index=[f"Recurso {i+1}" for i in range(int(num_resources))]
            )
            matrix.insert(0, "Recurso", matrix.index)  # Add index as a column

            # Configure editable table with AgGrid
            st.subheader("Editar datos manualmente")
            gb = GridOptionsBuilder.from_dataframe(matrix)
            gb.configure_default_column(editable=True)
            gb.configure_column("Recurso", editable=False)  # Make index non-editable
            grid_options = gb.build()

            response = AgGrid(
                matrix,
                gridOptions=grid_options,
                editable=True,
                fit_columns_on_grid_load=True,
            )

            # Retrieve entered data
            if st.button("Procesar datos manuales"):
                updated_matrix = pd.DataFrame(response["data"])
                st.write("Datos ingresados:")
                st.dataframe(updated_matrix)

    elif input_option == "Cargar desde CSV":
        # Upload CSV file
        st.subheader("Sube un archivo CSV")
        uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

        if uploaded_file is not None:
            # Read CSV file
            data = pd.read_csv(uploaded_file)
            
            # Display and edit CSV data
            st.subheader("Editar datos del CSV")
            gb = GridOptionsBuilder.from_dataframe(data)
            gb.configure_default_column(editable=True)
            grid_options = gb.build()

            response = AgGrid(
                data,
                gridOptions=grid_options,
                editable=True,
                fit_columns_on_grid_load=True,
                height=200,
            )

            # Retrieve edited data
            if st.button("Procesar datos del CSV"):
                edited_data = pd.DataFrame(response["data"])
                st.write("Datos editados:")
                st.dataframe(edited_data)

    # Option to save processed data
    if st.button("Descargar datos procesados"):
        if input_option == "Imputar manualmente" and 'response' in locals():
            data_to_download = pd.DataFrame(response["data"])
        elif input_option == "Cargar desde CSV" and 'response' in locals():
            data_to_download = pd.DataFrame(response["data"])
        else:
            data_to_download = None

        if data_to_download is not None:
            csv = data_to_download.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name="datos_procesados.csv",
                mime="text/csv",
            )
        else:
            st.warning("No hay datos procesados para descargar.")

app()
