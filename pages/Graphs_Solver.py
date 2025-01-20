import streamlit as st
import networkx as nx
from pyvis.network import Network

# Inicializar grafo y estado
if "graph" not in st.session_state:
    st.session_state["graph"] = nx.Graph()

st.title("Graph Drawing Interface")

columns = st.columns(3)

with columns[0]:
    # Inputs para agregar nodos y aristas
    st.sidebar.header("Add Elements")
    node = st.text_input("Add a node:")
    if st.button("Add Node"):
        if node:
            st.session_state["graph"].add_node(node)

with columns[1]:
    edge = st.text_input("Add an edge (format: node1,node2):")
    

with columns[2]:
    weight = st.number_input("Edge weight", min_value=0, value=1)
    
if st.button("Add Edge"):
    try:
        n1, n2 = edge.split(",")
        st.session_state["graph"].add_edge(n1, n2)
    except ValueError:
        st.error("Please enter the edge in the format 'node1,node2'.")

# Visualizar el grafo
st.header("Graph Visualization")
net = Network(notebook=True, height="500px", width="100%")
net.from_nx(st.session_state["graph"])
html = net.generate_html()

st.components.v1.html(html, height=500)
