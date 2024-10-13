"""
Fonction utiles pour la navigation
"""
import streamlit as st

from streamlit_utils.manage_state import *
from src.variables import *
from src.flow.arborescence.arborescence import Arborescence


def load_next_arborescence(prochaine_arborescence="Programme exemple"):
    # TODO Prochain programme
    st.session_state["arborescence"] = Arborescence(arborescence=prochaine_arborescence)
    st.session_state["select_option"] = None
    st.session_state['annee'] =  int(st.session_state.arborescence.question.annee)
    # Sauvegarder les indicateurs dans SQL
    # TODO récupérer les objets et les programmes
    # Mise à jour des objets depuis SQL
    update_indicateurs()
    get_objets_from_sql()
    get_programmes_from_sql()
