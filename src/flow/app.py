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


def create_objets(arborescence: str) -> None:
    df_objets = pd.read_csv(FICHIER_OBJETS[arborescence], sep=";")
    for _, row in df_objets.iterrows():
        new_objet = MyObjet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet


def go_to_next_arborescence():
    prochaine_arborescence = "Programme exemple"  # TODO Prochain programme
    st.session_state["arborescence"] = Arborescence(
        arborescence=prochaine_arborescence
    )
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
        go_to_next_arborescence() 
    else:
        st.session_state.arborescence.load_data(prochaine_question)
    st.rerun()

def buy_unit():
    """
    Achat d'un certain nombre d'unités
    """
    go_to_next_arborescence()
    objet_to_buy = st.session_state[t.session_state.arborescence.question.objet]
    st.session_state.sql_client.update_objet()

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
        page_title="Arborescence",
        page_icon="🧊",
        layout="wide",
    )
    # TODO page acceuil
    st.session_state["equipe"] = "test"
    st.session_state["arborescence"] = Arborescence(arborescence="Programme exemple")
    st.session_state["sql_client"] = ClientSQL("sql")
    create_objets(arborescence="Programme exemple")
    show()
