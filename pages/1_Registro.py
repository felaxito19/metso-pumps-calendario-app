import streamlit as st
from datetime import date, timedelta
from supabase import create_client, Client

# ============================================================
# CONECTAR A SUPABASE
# ============================================================
@st.cache_resource
def init_supabase():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase: Client = init_supabase()

#==============================================================
# CARGAR CATÁLOGOS
#==============================================================
def cargar_personas():
    resp = supabase.table("catalogo_personas").select("nombre").execute()
    return [row["nombre"] for row in (resp.data or [])]

def cargar_clientes():
    resp = supabase.table("catalogo_clientes").select("nombre").execute()
    return [row["nombre"] for row in (resp.data or [])]

# ============================================================
# GUARDAR EVENTO EN BD
# ============================================================
def guardar_evento(persona, cliente, fecha):
    data = {
        "persona": persona,
        "cliente": cliente,
        "fecha": fecha
    }
    supabase.table("BD_calendario_disponibilidad").insert(data).execute()

# ============================================================
# ESTADOS INICIALES
# ============================================================
if "post_guardado" not in st.session_state:
    st.session_state.post_guardado = False

if "default_persona" not in st.session_state:
    st.session_state.default_persona = None

if "default_cliente" not in st.session_state:
    st.session_state.default_cliente = None

if "default_rango" not in st.session_state:
    st.session_state.default_rango = None

# ============================================================
# UI PRINCIPAL
# ============================================================
st.title("📆 Registrar disponibilidad")

PERSONAS = cargar_personas()
CLIENTES = cargar_clientes()

# Usar valores por defecto si existen
persona_default = st.session_state.default_persona or PERSONAS[0]
cliente_default = st.session_state.default_cliente or CLIENTES[0]
rango_default = st.session_state.default_rango or date.today()

persona = st.selectbox("👤 Nombre del empleado", PERSONAS, key="persona_input",
                       index=PERSONAS.index(persona_default))

cliente = st.selectbox("🏢 Cliente", CLIENTES, key="cliente_input",
                       index=CLIENTES.index(cliente_default))

rango = st.date_input("📅 Seleccionar fecha o rango", 
                      key="rango_input",
                      value=rango_default)

# ============================================================
# BOTÓN GUARDAR
# ============================================================
if st.button("💾 Guardar"):

    # 1 SOLO DÍA
    if isinstance(rango, date):
        guardar_evento(persona, cliente, rango.isoformat())
    
    # RANGO COMPLETO
    elif isinstance(rango, tuple) and len(rango) == 2:
        inicio, fin = rango
        if fin < inicio:
            st.error("La fecha final no puede ser menor que la inicial.")
            st.stop()

        for d in range((fin - inicio).days + 1):
            dia = inicio + timedelta(days=d)
            guardar_evento(persona, cliente, dia.isoformat())

    else:
        st.error("Selecciona una fecha o un rango válido.")
        st.stop()

    # guardar estado
    st.session_state.post_guardado = True
    st.rerun()

# ============================================================
# MENSAJE DE ÉXITO
# ============================================================
if st.session_state.post_guardado:

    st.success("✔ Registro guardado correctamente.")
    st.write("¿Qué deseas hacer ahora?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔁 Agregar otra actividad"):

            # Reset de defaults
            st.session_state.default_persona = PERSONAS[0]
            st.session_state.default_cliente = CLIENTES[0]
            st.session_state.default_rango = date.today()

            # Reset widgets
            for k in ["persona_input", "cliente_input", "rango_input"]:
                if k in st.session_state:
                    del st.session_state[k]

            st.session_state.post_guardado = False
            st.rerun()

    with col2:
        if st.button("🚪 Salir"):
            st.write("Gracias por registrar la disponibilidad.")
            st.stop()
