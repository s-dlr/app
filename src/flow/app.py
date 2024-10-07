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

def login():
    st.header("Choix du nom de l'équipe")
    team = st.text_input("équipe", "astrolabe")
    button_login = st.button("Log in")
    if button_login:
        st.session_state["equipe"] = team
        st.rerun()

def create_objets(arborescence: str) -> None:
    df_objets = pd.read_csv(FICHIER_OBJETS[arborescence], sep=";")
    for _, row in df_objets.iterrows():
        new_objet = MyObjet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet

if __name__ == "__main__":
    # TODO page accueil
    if "equipe" not in st.session_state:
        st.session_state.equipe = None
        pg = st.navigation(
            [
                st.Page(
                    login,
                    title="Choix équipe",
                    icon=":material/handyman:"
                )
            ]
        )
    else:
        st.session_state["sql_client"] = ClientSQL(
            connection_name="sql", equipe=st.session_state.equipe
        )
        st.session_state["arborescence"] = Arborescence(arborescence="Programme exemple")
        create_objets(arborescence="Programme exemple")
        pg = st.navigation(
            [
                st.Page(
                        "page_arborescence.py",
                        title="Arborescence",
                        icon="🧊"
                )
            ]
       )

    pg.run()
