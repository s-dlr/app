import sys

import pandas as pd
import streamlit as st

sys.path.append(".")

from src.sql_client import *
from src.variables import *
from src.flow.arborescence.arborescence import Arborescence
from src.flow.views.options_view import OptionsView
from src.flow.views.buy_view import BuyView
from src.data.objet import MyObjet

def go_to_next_arborescence():
    prochaine_arborescence = "Programme exemple"  # TODO Prochain programme
    st.session_state["arborescence"] = Arborescence(arborescence=prochaine_arborescence)
    create_objets(arborescence=prochaine_arborescence)


def go_to_next_question():
    """
    Fonction pour passer à la question suivante
    1. Mise à jour  de l'état de l'arborecence (question et options courantes)
    2. Mise à jour de la vue
    """
    selected_option = st.session_state.radio_options
    prochaine_question = st.session_state.arborescence.question.get_next_question(
        selected_option
    )
    if prochaine_question == 0:
        start_programme()
        go_to_next_arborescence()
    else:
        st.session_state.arborescence.load_data(prochaine_question)
    st.rerun()


def start_programme():
    """
    Démarrage du programme
    """
    # écupérer le nom de l'objet que concerne le programme
    nom_objet_programme = "default_object"
    # Mise à jour de l'objet en cours de définition
    objet_programme = st.session_state[nom_objet_programme]
    st.session_state.sql_client.update_sql_objet(objet_programme)
    # Démarrage programme


def buy_unit():
    """
    Achat d'un certain nombre d'unités
    """
    objet_achete = st.session_state[st.session_state.arborescence.question.objet]
    st.session_state.sql_client.update_sql_objet(objet_achete)
    go_to_next_arborescence()


@st.fragment
def show() -> None:
    if st.session_state.arborescence.type_question == CHOIX_OPTION:
        st.session_state["view"] = OptionsView()
        st.session_state.view.show()
        st.session_state.view.display_button(
            on_click=go_to_next_question, disabled=(not st.session_state.radio_options)
        )
    elif st.session_state.arborescence.type_question == CHOIX_NOMBRE_UNITE:
        st.session_state["view"] = BuyView()
        st.session_state.view.show()
        st.session_state.view.display_button(on_click=buy_unit)


if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
    )
    show()
