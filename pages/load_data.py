import streamlit as st

from streamlit_utils.manage_state import init_objets, init_programmes
from streamlit_utils.navigation import load_next_arborescence

st.set_page_config(
    page_title="Chargement des aroborescences",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "equipe" in st.session_state:
    st.header("Charger les donneés du prochain programme")

    uploaded_arborescence = st.file_uploader("Choisir une arborescence")
    uploaded_objets = st.file_uploader("Choisir un fichier objet")
    uploaded_programmes = st.file_uploader("Choisir un fichier programme")

    if st.button("Charger les données", type="primary"):
        load_next_arborescence(uploaded_arborescence)
        init_objets(uploaded_objets)
        init_programmes(uploaded_programmes)
        st.success("L'arborescence et les objets ont été créés")

    st.page_link("pages/options.py", label="Commencer", icon=":material/settings:")
else:
    st.write("Aucune partie en cours. Connectez vous d'abord.")
    st.page_link("pages/login.py", label="Se connecter", icon="🏠")
