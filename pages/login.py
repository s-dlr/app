import sys

sys.path.append(".")

import pandas as pd
import streamlit as st
from sqlalchemy.sql import text

from src.data.indicateurs import *
from streamlit_utils.manage_state import *
from src.variables import *
from src.sql_client import ClientSQL
from streamlit_utils.navigation import *

st.set_page_config(
    page_title="Login", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed"
)

def delete_team_in_db(equipe) -> None:
    queries_delete = [
        f'DELETE FROM `Indicateurs` WHERE equipe={equipe};'
        f'DELETE FROM `Armee` WHERE equipe={equipe};'
        f'DELETE FROM `Constructions` WHERE equipe={equipe};'
        f'DELETE FROM `Programmes` WHERE equipe={equipe};'
        f'DELETE FROM `Objets` WHERE equipe={equipe};'
        f'DELETE FROM `Etat` WHERE equipe={equipe};    '
    ]
    connection = st.connection("astrolabedb", autocommit=True, ttl=1)
    with connection.session as session:
        for query in queries_delete:
            session.execute(text(query))
        session.commit()

def init_team_in_db() -> None:
    """
    Créatoin de l'équipe dans la base de données
    """
    st.session_state["sql_client"] = ClientSQL(
        connection_name="astrolabedb", equipe=st.session_state.equipe
    )
    df_etat_equipe = st.session_state.sql_client.get_table("Etat")
    if df_etat_equipe.shape[0] > 0:
        etat_equipe = df_etat_equipe.iloc[0].to_dict()
        st.success(
            f"Chargement du jeu là où vous vous étiez arrêtés ({etat_equipe[ARBORESCENCE]}, question {etat_equipe[QUESTION]})"
        )
        get_indicateurs_from_sql()
        return etat_equipe
    else:
        st.session_state["annee"] = 1990
        st.session_state["indicateurs"] = Indicateurs(annee=st.session_state.annee)
        st.session_state["armee"] = Armee(annee=st.session_state.annee)
        st.session_state.indicateurs.send_to_sql(st.session_state.sql_client)
        st.session_state.armee.send_to_sql(st.session_state.sql_client)
        push_etat_to_sql(list(ARBORESCENCES.keys())[0], 1)
        return {ARBORESCENCE: list(ARBORESCENCES.keys())[0], QUESTION: 1}

# Affichage
st.header("Choix du nom de l'équipe")
team = st.text_input("équipe", "astrolabe")

login = st.button("Log in", type="primary")
delete_equipe = st.checkbox("Recommencer depuis le début")

if login:
    st.session_state["equipe"] = team
    if delete_equipe:
        delete_team_in_db(team)
    etat_equipe = init_team_in_db()
    load_next_arborescence(
        prochaine_arborescence=etat_equipe[ARBORESCENCE],
        num_question=etat_equipe[QUESTION],
    )
    st.switch_page("pages/options.py")
