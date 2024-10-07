import sys

import pandas as pd
import streamlit as st

from src.sql_client import *
from src.variables import *
from src.flow.arborescence.arborescence import Arborescence
from src.flow.arborescence.option import Option
from src.flow.views.options_view import OptionsView
from src.flow.views.buy_view import BuyView
from src.data.objet import Objet


def create_objets() -> None:
    df_objets = pd.read_csv(FICHIER_OBJETS, sep=";")
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet


def go_to_next_arborescence():
    prochaine_arborescence = "Programme exemple"  # TODO Prochain programme
    st.session_state["arborescence"] = Arborescence(arborescence=prochaine_arborescence)
    # Mise à jour des objets depuis SQL


def go_to_next_question():
    """
    Fonction pour passer à la question suivante
    1. Mise à jour  de l'état de l'arborecence (question et options courantes)
    2. Mise à jour de la vue
    """
    selected_option_text = st.session_state.radio_options
    selected_option = st.session_state.arborescence.question.get_option_by_text(
        selected_option_text
    )
    # Mise à jour de l'objet
    # Mise à jour du programme
    if selected_option.prochaine_question == 0:
        start_programme(selected_option)
        go_to_next_arborescence()
    else:
        st.session_state.arborescence.load_data(selected_option.prochaine_question)


def start_programme(option: Option):
    """
    Démarrage du programme
    """
    # Sauvegarde de l'objet dans la base SQL
    objet_programme = st.session_state[option.objet]
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
def init_show() -> None:
    if "equipe" not in st.session_state:
        st.header("Choix du nom de l'équipe")
        team = st.text_input("équipe", "astrolabe")
        if st.button("Log in"):
            st.session_state["equipe"] = team
            st.session_state["sql_client"] = ClientSQL(
                connection_name="sql", equipe=st.session_state.equipe
            )
            st.rerun()
    else:
        show()
        
@st.fragment
def show() -> None:
    if st.session_state.arborescence.type_question == CHOIX_OPTION:
        st.session_state["view"] = OptionsView()
        st.session_state.view.show()
        st.session_state.view.display_button(
            on_click=go_to_next_question, disabled=(not st.session_state.radio_options)
        )
        st.rerun()
    elif st.session_state.arborescence.type_question == CHOIX_NOMBRE_UNITE:
        st.session_state["view"] = BuyView()
        st.session_state.view.show()
        st.session_state.view.display_button(on_click=buy_unit)
        st.rerun()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Arborescence",
        page_icon="🧊",
        layout="wide",
    )
    # Initialisation objets et arborescence
    create_objets()
    go_to_next_arborescence()
    # Affichage
    show()
