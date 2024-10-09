"""
Fonction utiles pour la navigation
"""
import streamlit as st

from src.variables import *
from src.flow.arborescence.arborescence import Arborescence

def load_next_arborescence():
    prochaine_arborescence = "Programme exemple"  # TODO Prochain programme
    st.session_state["arborescence"] = Arborescence(arborescence=prochaine_arborescence)
    # Mise à jour des objets depuis SQL

def go_to_next_question():
    """
    Fonction pour passer à la question suivante
    1. Mise à jour  de l'état de l'arborecence (question et options courantes)
    2. Mise à jour de la vue
    """
    # Etat de l'arborescence
    if st.session_state.arborescence:
        next_question = st.session_state.arborescence.get_next_question(st.session_state.option)
        if next_question == 0:
            load_next_arborescence()
        else:
            st.session_state.arborescence.load_data(next_question)
    else:
        load_next_arborescence()
