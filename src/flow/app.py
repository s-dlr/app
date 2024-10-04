import sys

import pandas as pd
import streamlit as st

sys.path.append(".")

from src.variables import *
from src.flow.arborescence.arborescence import Arborescence
from src.flow.views.options_view import OptionsView
from src.flow.views.buy_view import BuyView
from src.data.object import MyObject


def create_objects(arborescence: str) -> None:
    df_objects = pd.read_csv(FICHIER_OBJETS[arborescence], sep=";")
    for _, row in df_objects.iterrows():
        new_object = MyObject(**row.to_dict())
        st.session_state[row[NOM]] = new_object

def go_to_next_arborescence():
    prochaine_arborescence = "Programme exemple"  # TODO Prochain programme
    st.session_state["arborescence"] = Arborescence(
        arborescence=prochaine_arborescence
    )
    create_objects(arborescence=prochaine_arborescence)

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
        go_to_next_arborescence() 
    else:
        st.session_state.arborescence.load_data(prochaine_question)
    st.rerun()

def buy_unit():
    """
    Achat d'un certain nombre d'unités
    """
    go_to_next_arborescence() 

@st.fragment
def show() -> None:
    if st.session_state.arborescence.question.type == CHOIX_OPTION:
        st.session_state["view"] = OptionsView()
        st.session_state.view.show()
        st.session_state.view.display_button(
            on_click=go_to_next_question, disabled=(not st.session_state.radio_options)
        )
    elif st.session_state.arborescence.question.type == CHOIX_NOMBRE_UNITE:
        st.session_state["view"] = BuyView()
        st.session_state.view.show()
        st.session_state.view.display_button(on_click=buy_unit)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Arborescence",
        page_icon="🧊",
        layout="wide",
    )
    st.session_state["arborescence"] = Arborescence(arborescence="Programme exemple")
    create_objects(arborescence="Programme exemple")
    show()
