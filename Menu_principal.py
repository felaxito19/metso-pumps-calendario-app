import streamlit as st


st.set_page_config(
    page_title="Sistema de Disponibilidad",
    page_icon="📌",
    layout="centered"
)

st.title("Seguimiento - Visitas a minas")
st.write("Bienvenido al panel principal. Usa el menú de la izquierda para registrar actividades o visualizar el calendario.")

# ======== DISEÑO VERTICAL ==========

st.header("👋 Bienvenido")
st.write("Este sistema permite dar seguimiento y visualizar las visitas del equipo en las unidades mineras")

# SECCIÓN 1

st.markdown("""
### 📝 Registrar visitas  
- Seleccionar tu nombre 
- Elegir la unidad minera  
- Registrar las fechas de visita  
- Guardar la actividad en la base de datos  

<br>
""", unsafe_allow_html=True)

# SECCIÓN 2
st.markdown("""
### 📅 Ver calendario  
Podras filtrar el usuario y/o la unidad minera para visualizar las visitas programadas.  

<br><br>
""", unsafe_allow_html=True)



