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
        selected_option = st.session_state.arborescence.question.get_option_by_text(
            st.session_state.radio_options
        )
        if selected_option.prochaine_question == 0:
            load_next_arborescence()
        else:
            st.session_state.arborescence.load_data(selected_option.prochaine_question)
    else:
        load_next_arborescence()
    st.write(st.session_state.arborescence.type_question)
