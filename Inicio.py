import streamlit as st

# Página de inicio
def main():
    st.title("Bienvenido al Solver de Programación Lineal")
    st.write("""
    Resuelve fácilmente problemas de programación lineal utilizando nuestra herramienta interactiva.
    Escoge el tipo de solver desde la barra lateral.
    """)

    st.image("images/xd.png", caption="Resolver problemas de programación lineal fácilmente.")

if __name__ == "__main__":
    main()