"""
Fonction utiles pour la navigation
"""
import streamlit as st

from src.variables import *
from src.flow.arborescence.arborescence import Arborescence


def load_next_arborescence(prochaine_arborescence="Programme exemple"):
    # TODO Prochain programme
    st.session_state["arborescence"] = Arborescence(
        arborescence=st.session_state["arborescence_file"]
    )
    # Mise à jour des objets depuis SQL
    st.session_state["select_option"] = None
    st.session_state['annee'] =  st.session_state.arborescence.df_arborescence[ANNEE].iloc[0]
    # TODO Si néccessaire
    # Appliquer les programmes et les constructions en cours
    # Sauvegarder les indicateurs dans SQL


def go_to_next_question():
    """
    Fonction pour passer à la question suivante
    1. Mise à jour  de l'état de l'arborecence (question et options courantes)
    2. Mise à jour de la vue
    """
    if "select_option" not in st.session_state:
        st.session_state["select_option"] = None
    # Etat de l'arborescence
    if st.session_state.arborescence:
        next_question = st.session_state.arborescence.get_next_question(
            st.session_state.select_option
        )
        if next_question != 0:
            st.session_state.arborescence.load_data(next_question)
        else:
            st.session_state.arborescence = False
    else:
        st.session_state.arborescence = False
