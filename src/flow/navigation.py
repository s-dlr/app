"""
Fonction utiles pour la navigation
"""
import streamlit as st

from src.flow.arborescence.arborescence import Arborescence

def go_to_next_arborescence():
    prochaine_arborescence = "Programme exemple"  # TODO Prochain programme
    st.session_state["arborescence"] = Arborescence(arborescence=prochaine_arborescence)
    # Mise à jour des objets depuis SQL
