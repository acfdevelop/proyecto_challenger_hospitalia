import streamlit as st

from agente import ejecutar_agente
from rag import inicializar

st.set_page_config(page_title="HospitalIA", page_icon="🏥")

if "inicializado" not in st.session_state:
    inicializar()
    st.session_state.inicializado = True

if "pregunta" not in st.session_state:
    st.session_state.pregunta = ""

st.title("🏥 HospitalIA")

st.subheader("Preguntas frecuentes")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏥 ¿Qué necesito para hospitalizarme?"):
        st.session_state.pregunta = "¿Qué necesito para hospitalizarme?"
        st.session_state.consultar = True

    if st.button("📄 ¿Cuáles son los derechos del paciente?"):
        st.session_state.pregunta = "¿Cuáles son los derechos del paciente?"
        st.session_state.consultar = True

with col2:
    if st.button("📞 ¿Cómo puedo presentar un reclamo?"):
        st.session_state.pregunta = "¿Cómo puedo presentar un reclamo?"
        st.session_state.consultar = True

    if st.button("🕒 ¿Cuáles son los horarios de visita?"):
        st.session_state.pregunta = "¿Cuáles son los horarios de visita?"
        st.session_state.consultar = True

pregunta = st.text_input(
    "Escribe tu consulta",
    key="pregunta"
)

if st.button("Consultar"):
    st.session_state.consultar = True

if st.session_state.get("consultar", False):

    st.session_state.consultar = False

    with st.spinner("Consultando documentación..."):
        respuesta = ejecutar_agente(st.session_state.pregunta)

    st.success("Respuesta")
    st.write(respuesta)