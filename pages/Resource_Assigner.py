import streamlit as st
from models import ResourceAssigner

def app():
    st.title("Resource Assigner")
    st.write("This page is for assigning resources to tasks.")

    # Create a new ResourceAssigner object
    ra = ResourceAssigner()

    # Display the ResourceAssigner object
    st.write(ra)

    # Display the ResourceAssigner object's methods
    st.write(dir(ra))