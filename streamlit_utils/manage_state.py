"""
Mises jour du session state
"""
import pandas as pd
import streamlit as st

from src.data.objet import Objet
from src.data.programme import Programme
from src.data.indicateurs import *
from src.variables import *


def init_objets(fichier_objets=FICHIER_OBJETS) -> None:
    """
    Récupération des objets
    """
    # Objets en local
    df_objets = pd.read_csv(fichier_objets, sep=";")
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet
    # Objets SQL
    get_objets_from_sql()


def init_programmes(fichier_programmes=FICHIER_PROGRAMMES) -> None:
    """
    Récupération des objets
    """
    # Programmes en local
    df_programmes = pd.read_csv(fichier_programmes, sep=";")
    for _, row in df_programmes.iterrows():
        new_programme = Programme(**row.to_dict())
        st.session_state["programme_"+row[NOM]] = new_programme
    # Programmes SQL
    get_programmes_from_sql()


def get_programmes_from_sql() -> None:
    """
    Récupère les objets de l'équipe dans la base SQL
    Si l'objet existe déjà dans le sessin_state, il est écrasé
    """
    df_objets = st.session_state.sql_client.get_table("Programmes")
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet


def get_objets_from_sql() -> None:
    """
    Récupère les objets de l'équipe dans la base SQL
    Si l'objet existe déjà dans le sessin_state, il est écrasé
    """
    df_objets = st.session_state.sql_client.get_table("Objets")
    for _, row in df_objets.iterrows():
        new_objet = Objet(**row.to_dict())
        st.session_state[row[NOM]] = new_objet

def get_indicateurs_from_sql() -> None:
    """
    Mise à jour ou créations des indicateurs à partir de SQL
    """
    df_indicateurs = st.session_state.sql_client.get_last_value("Indicateurs")
    st.session_state["indicateurs"] = Indicateurs(**df_indicateurs.iloc[0].to_dict())
    df_armee = st.session_state.sql_client.get_last_value("Armee")
    st.session_state["armee"] = Armee(**df_armee.iloc[0].to_dict())

def update_indicateurs() -> None:
    get_indicateurs_from_sql()
    # TODO Si nécessaire
    # Appliquer les programmes et les constructions en cours
    if st.session_state.annee > st.session_state.indicateurs.annee:
        # TODO if modification
        st.session_state.indicateurs.send_to_sql(st.session_state.sql_client)
    if st.session_state.annee > st.session_state.armee.annee:
        # TODO if modification
        st.session_state.armee.send_to_sql(st.session_state.sql_client)

def launch_programme(programme) -> None:
    st.session_state[programme].create_start_end(st.session_state.annee)
    st.session_state[programme].send_to_sql(st.session_state.sql_client)
