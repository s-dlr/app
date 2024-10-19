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
    df_etat_equipe = st.session_state.sql_client.get_table("Etat")
    if df_etat_equipe.shape[0] > 0:
        get_indicateurs_from_sql()
    else:
        st.session_state["annee"] = 2000
        st.session_state["indicateurs"] = Indicateurs(annee=st.session_state.annee)
        st.session_state["armee"] = Armee(annee=st.session_state.annee)
        st.session_state.indicateurs.send_to_sql(st.session_state.sql_client)
        st.session_state.armee.send_to_sql(st.session_state.sql_client)
        df_etat_equipe[ARBORESCENCE] = list(ARBORESCENCES.keys())[0]
        df_etat_equipe[QUESTION] = 1
    return df_etat_equipe.iloc[0]

# Affichage
st.header("Choix du nom de l'équipe")
team = st.text_input("équipe", "astrolabe")

if st.button("Log in", type="primary"):
    st.session_state["equipe"] = team
    etat_equipe = init_team_in_db()
    load_next_arborescence(etat_equipe[ARBORESCENCE], etat_equipe[QUESTION])
    st.switch_page("pages/options.py")
