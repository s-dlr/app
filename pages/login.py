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
    st.write(f"SELECT * FROM `Etat` WHERE `equipe` = '{st.session_state.equipe}'")
    st.write(df_etat_equipe)
    if df_etat_equipe.shape[0] > 0:
        etat_equipe = df_etat_equipe.iloc[0].to_dict()
        st.success(
            f"Chargement du jeu là où vous vous étiez arrêtés ({etat_equipe[ARBORESCENCE]}, question {etat_equipe[QUESTION]})"
        )
        get_indicateurs_from_sql()
        return df_etat_equipe.iloc[0].to_dict()
    else:
        st.session_state["annee"] = 2000
        st.session_state["indicateurs"] = Indicateurs(annee=st.session_state.annee)
        st.session_state["armee"] = Armee(annee=st.session_state.annee)
        st.session_state.indicateurs.send_to_sql(st.session_state.sql_client)
        st.session_state.armee.send_to_sql(st.session_state.sql_client)
        return {ARBORESCENCE: list(ARBORESCENCES.keys())[0], QUESTION: 1}

# Affichage
st.header("Choix du nom de l'équipe")
team = st.text_input("équipe", "astrolabe")

if st.button("Log in", type="primary"):
    st.session_state["equipe"] = team
    etat_equipe = init_team_in_db()
    load_next_arborescence(
        prochaine_arborescence=etat_equipe[ARBORESCENCE],
        num_question=int(etat_equipe[QUESTION]),
    )
    push_etat_to_sql(etat_equipe[ARBORESCENCE], etat_equipe[QUESTION])
    st.switch_page("pages/options.py")
