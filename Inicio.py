import streamlit as st

# Opciones que se mostrarán en LaTeX
latex_options = [
    r"$Opción\ 1$", 
    r"$Opción\ 2$", 
    r"$Opción\ 3$"
]

# Mostrar las opciones en formato LaTeX con st.markdown()
for option in latex_options:
    st.markdown(f"Selecciona: {option}")

# Crear el selector múltiple tradicional
options = ['Opción 1', 'Opción 2', 'Opción 3']
selected_options = st.multiselect("Selecciona una opción", options)

# Mostrar las opciones seleccionadas
st.write(f"Opciones seleccionadas: {selected_options}")
