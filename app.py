import sys

import pandas as pd
import streamlit as st

sys.path.append(".")

from src.sql_client import *
from src.variables import *
from src.flow.arborescence.arborescence import Arborescence
from src.data.objet import MyObjet

def login():
    st.header("Choix du nom de l'équipe")
    team = st.text_input("équipe", "astrolabe")
    if st.button("Log in"):
        st.session_state["equipe"] = team
        st.rerun(scope="app")

def start_game():
    st.session_state["sql_client"] = ClientSQL(
        connection_name="sql", equipe=st.session_state.equipe
    )
    st.session_state["arborescence"] = Arborescence(arborescence="Programme exemple")
    create_objets(arborescence="Programme exemple")
    # st.switch_page("pages/page_arborescence.py")


def create_objets(arborescence: str) -> None:
    df_objets = pd.read_csv(FICHIER_OBJETS[arborescence], sep=";")
    for _, row in df_objets.iterrows():
        new_objet = MyObjet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet


if __name__ == "__main__":
    # TODO page accueil
    st.set_page_config(initial_sidebar_state="collapsed")
    if "equipe" not in st.session_state:
        pg = st.navigation([st.Page(login)])
    else:
        start_game()
        pg = st.navigation([st.Page("streamlit_pages/page_arborescence.py")])
    pg.run()