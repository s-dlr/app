import sys

sys.path.append(".")

import pandas as pd
import streamlit as st

from src.data.indicateurs import *
from src.data.objet import Objet
from src.variables import *
from src.sql_client import ClientSQL
from src.flow.navigation import *

def init_objets() -> None:
    # Objets en local
    df_objets = pd.read_csv(FICHIER_OBJETS, sep=";")
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet
    # Objets SQL
    # TODO: récupérer les objets existants

def init_team_in_db() -> None:
    """
    Créatoin de l'équipe dans la base de données
    """
    st.session_state["sql_client"] = ClientSQL(
        connection_name="astrolabedb", equipe=st.session_state.equipe
    )
    df_indicateurs = st.session_state.sql_client.get_last_value("Indicateurs")
    # Si l'équipe existe déjà
    if df_indicateurs.shape[0] > 0:
        # Récupérer les derniers indicateurs connus
        st.session_state["indicateurs"] = Indicateurs(**df_indicateurs.iloc[0].to_dict())
        df_armee = st.session_state.sql_client.get_last_value("Armee")
        st.session_state["armee"] = Armee(**df_armee.iloc[0].to_dict())
    # Sinon initialisation
    else:
        st.session_state["indicateurs"] = Indicateurs(annee=st.session_state.annee)
        st.session_state["armee"] = Armee(annee=st.session_state.annee)
        # Sauvegarde des indicateurs dans SQL
        st.session_state.sql_client.insert_row(
            table="Indicateurs",
            value_dict=st.session_state.indicateurs.to_dict(),
        )
        st.session_state.sql_client.insert_row(
            table="Armee", value_dict=st.session_state.armee.to_dict()
        )

st.set_page_config(
    page_title="Login", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed"
)


# Affichage
st.header("Choix du nom de l'équipe")
team = st.text_input("équipe", "astrolabe")

if st.button("Log in", type="primary"):
    st.session_state["equipe"] = team
    load_next_arborescence()
    init_team_in_db()
    init_objets()
    if st.session_state.arborescence.type_question == CHOIX_OPTION:
        st.switch_page("pages/options.py")
    elif st.session_state.arborescence.type_question == CHOIX_NOMBRE_UNITE:
        st.switch_page("pages/buy.py")
