import streamlit as st

from pages.login import init_objets
from src.flow.navigation import load_next_arborescence

st.header("Charger les donneés du prochain programme")

uploaded_arborescence = st.file_uploader("Choisir une arborescence")
uploaded_objets = st.file_uploader("Choisir un fichier objet")

init_objets(uploaded_objets)
load_next_arborescence(uploaded_arborescence)
