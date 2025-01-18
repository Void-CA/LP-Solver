import streamlit as st
import pandas as pd
from models import ResourceAssignmentSolver
from st_aggrid import AgGrid, GridOptionsBuilder

# Usar CSS para modificar el tamaño del contenedor del gráfico
st.markdown(
    """
    <style>
        .block-container {
            max-width: 900px;  # Ajusta el ancho según lo desees
        }
    </style>
    """, unsafe_allow_html=True)

def app():

    st.title("Solver de Asignación de Recursos")

    # Opción: Imputar datos o cargar CSV
    opcion = st.radio("Selecciona cómo ingresar los datos:", ("Imputar manualmente", "Cargar desde CSV"), horizontal=True)

    if opcion == "Imputar manualmente":
        # Pedir dimensiones de la tabla
        num_recursos = st.number_input("Cantidad de recursos", min_value=1, step=1, value=3)
        num_trabajadores = st.number_input("Cantidad de trabajadores", min_value=1, step=1, value=3)

        # Crear DataFrame inicial vacío
        if num_recursos > 0 and num_trabajadores > 0:
            matriz = pd.DataFrame(
                [[0 for _ in range(int(num_trabajadores))] for _ in range(int(num_recursos))],
                columns=[f"Trabajador {i+1}" for i in range(int(num_trabajadores))],
                index=[f"Recurso {i+1}" for i in range(int(num_recursos))]
            )
            matriz.insert(0, "Recurso", matriz.index)  # Agregar índice como columna

            # Configurar tabla editable con AgGrid
            st.subheader("Editar datos manualmente")
            gb = GridOptionsBuilder.from_dataframe(matriz)
            gb.configure_default_column(editable=True)
            gb.configure_column("Recurso", editable=False)  # Hacer el índice no editable
            grid_options = gb.build()

            response = AgGrid(
                matriz,
                gridOptions=grid_options,
                editable=True,
                fit_columns_on_grid_load=True,
            )

            # Recuperar datos ingresados
            if st.button("Procesar datos manuales"):
                matriz_actualizada = pd.DataFrame(response["data"])
                st.write("Datos ingresados:")
                st.dataframe(matriz_actualizada)

    elif opcion == "Cargar desde CSV":
        # Subir archivo CSV
        st.subheader("Sube un archivo CSV")
        uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

        if uploaded_file is not None:
            # Leer archivo CSV
            data = pd.read_csv(uploaded_file)
            
            # Mostrar y editar los datos del CSV
            st.subheader("Editar datos del CSV")
            gb = GridOptionsBuilder.from_dataframe(data)
            gb.configure_default_column(editable=True)
            grid_options = gb.build()

            response = AgGrid(
                data,
                gridOptions=grid_options,
                editable=True,
                fit_columns_on_grid_load=True,
            )

            # Recuperar datos editados
            if st.button("Procesar datos del CSV"):
                data_editada = pd.DataFrame(response["data"])
                st.write("Datos editados:")
                st.dataframe(data_editada)

    # Opción para guardar los datos procesados
    if st.button("Descargar datos procesados"):
        if opcion == "Imputar manualmente" and 'response' in locals():
            datos_a_descargar = pd.DataFrame(response["data"])
        elif opcion == "Cargar desde CSV" and 'response' in locals():
            datos_a_descargar = pd.DataFrame(response["data"])
        else:
            datos_a_descargar = None

        if datos_a_descargar is not None:
            csv = datos_a_descargar.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name="datos_procesados.csv",
                mime="text/csv",
            )
        else:
            st.warning("No hay datos procesados para descargar.")

app()