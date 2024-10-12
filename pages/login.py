import sys

sys.path.append(".")

import pandas as pd
import streamlit as st

from src.data.indicateurs import *
from streamlit_utils.manage_state import *
from src.variables import *
from src.sql_client import ClientSQL
from streamlit_utils.navigation import *

st.set_page_config(
    page_title="Login", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed"
)


def init_team_in_db() -> None:
    """
    Créatoin de l'équipe dans la base de données
    """
    st.session_state["sql_client"] = ClientSQL(
        connection_name="astrolabedb", equipe=st.session_state.equipe
    )
    if st.session_state.sql_client:
        get_indicateurs_from_sql()
    else:
        st.session_state["annee"] = 2000
        st.session_state["indicateurs"] = Indicateurs(annee=st.session_state.annee)
        st.session_state["armee"] = Armee(annee=st.session_state.annee)
        st.session_state.indicateurs.send_to_sql(st.session_state.sql_client)
        st.session_state.armee.send_to_sql(st.session_state.sql_client)


# Affichage
st.header("Choix du nom de l'équipe")
team = st.text_input("équipe", "astrolabe")

if st.button("Log in", type="primary"):
    st.session_state["equipe"] = team
    init_team_in_db()
    st.session_state["arborescence"] = False
    st.switch_page("pages/load_data.py")
    # load_next_arborescence()
    # init_team_in_db()
    # init_objets()
    # if st.session_state.arborescence.type_question == CHOIX_OPTION:
    #     st.switch_page("pages/options.py")
    # elif st.session_state.arborescence.type_question == CHOIX_NOMBRE_UNITE:
    #     st.switch_page("pages/buy.py")
