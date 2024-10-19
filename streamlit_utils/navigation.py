"""
Fonction utiles pour la navigation
"""
import streamlit as st

from streamlit_utils.manage_state import *
from src.variables import *
from src.flow.arborescence.arborescence import Arborescence


def load_next_arborescence(prochaine_arborescence, num_question=1):
    # Prochain programme
    st.session_state["arborescence"] = Arborescence(
        arborescence=prochaine_arborescence, num_question=num_question
    )
    st.session_state["select_option"] = None
    st.session_state['annee'] =  int(st.session_state.arborescence.question.annee)
    st.session_state["prochaine_arborescence"] = PROCHAINES_ARBORESCENCE.get(
        prochaine_arborescence
    )
    # Création des objets de l'arborescence
    init_objets(FICHIERS_OBJETS[prochaine_arborescence])
    init_programmes(FICHIERS_PROGRAMMES[prochaine_arborescence])
    # Mise à jour des objets depuis SQL
    update_indicateurs()
