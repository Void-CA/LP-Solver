import streamlit as st

# Página de inicio
def main():
    st.title("Solver de Programación Lineal")
    st.write("""
    Resuelve fácilmente problemas de programación lineal utilizando nuestra herramienta interactiva.
    Escoge el tipo de solver desde la barra lateral.
    """)
    
    st.subheader("Problemas de Restricciones Lineales")
    st.write("Este módulo permite resolver problemas de optimización lineal en los que se busca maximizar o minimizar una función objetivo sujeta a un conjunto de restricciones lineales. Es ideal para problemas de planificación, producción, y asignación de recursos. Incluye una interfaz interactiva para ingresar las variables, restricciones, y parámetros, generando soluciones óptimas con pasos detallados.")
    with st.columns(3)[1]:
        st.image("images/linear_constraints.png", width=300)

    st.subheader("Asignación de Recursos")
    st.write("Este módulo permite resolver problemas de asignación de recursos en los que se busca asignar tareas a trabajadores de manera óptima. Es ideal para problemas de programación de la producción, asignación de personal, y logística. Incluye una interfaz interactiva para ingresar los datos, generando soluciones óptimas con pasos detallados.")
    with st.columns(3)[1]:
        st.image("images/resource_assignment.png", width=300)

    st.subheader("Grafos")
    st.write("""
            Este solver está orientado a problemas de asignación en los que se deben distribuir 
            recursos limitados de manera óptima entre múltiples tareas o categorías. 
            Es ideal para casos como asignación de personal, planificación de proyectos o distribución de presupuestos.
            Ofrece herramientas para personalizar los criterios de optimización y restricciones específicas.
             """)
    with st.columns(3)[1]:
        st.image("images/graphs.png", width=300 )

    st.subheader("Manejo de Proyectos")
    st.write("""
            Este módulo permite resolver problemas de ruta crítica en proyectos de construcción,
            planificación de eventos, y gestión de proyectos. Incluye una interfaz interactiva para
            ingresar las actividades, tiempos, y dependencias, generando el camino crítico y la duración
            del proyecto con pasos detallados.
            """)
    
    with st.columns(3)[1]:
        st.image("images/cpm.png", width=300)
    
    st.subheader("Trafico de redes (???)")
    st.write("No se si voy a hacer este, veremos")

if __name__ == "__main__":
    main()