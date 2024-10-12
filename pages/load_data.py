import streamlit as st

from pages.login import init_objets
from src.flow.navigation import load_next_arborescence

st.header("Charger les donneés du prochain programme")

uploaded_arborescence = st.file_uploader("Choisir une arborescence")
uploaded_objets = st.file_uploader("Choisir un fichier objet")

# if st.button("Charger les données", type="primary"):
if st.page_link("pages/options.py", label="Commencer", icon=":material/settings:"):
    load_next_arborescence(uploaded_arborescence)
    init_objets(uploaded_objets)

# st.page_link("pages/options.py", label="Commencer", icon=":material/settings:")
