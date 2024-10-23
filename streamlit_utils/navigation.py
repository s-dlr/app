"""
Fonction utiles pour la navigation
"""
import streamlit as st

from streamlit_utils.manage_state import *
from src.variables import *
from src.flow.arborescence.arborescence import Arborescence

def get_etat_satellite_2():
    query = f'SELECT * FROM `Etat` WHERE `equipe` = "{st.session_state.equipe}_satellite_2";'
    connection = st.session_state.sql_client.connection
    etat_satellite = connection.query(query, ttl=1)
    if etat_satellite.shape[0] > 0:
        return etat_satellite["question"].iloc[0]
    else:
        return False

def push_etat_satellite_2(next_question):
    query = f'INSERT INTO `Etat`(`equipe`, `arborescence`, `question`) VALUES ("{st.session_state.equipe}_satellite_2","","{next_question}")'
    st.session_state.sql_client.execute_query([query])

def load_next_arborescence(prochaine_arborescence, num_question=1):
    # Cas particulier des satellites
    if prochaine_arborescence == "Satellites phase 2":
        num_question = get_etat_satellite_2()
        if not num_question:
            prochaine_arborescence = PROCHAINES_ARBORESCENCE.get(prochaine_arborescence)
    # Chargement du prochain programme
    st.success(f"Chargement de {prochaine_arborescence}")
    try:
        st.session_state["arborescence"] = Arborescence(
            arborescence=prochaine_arborescence, num_question=num_question
        )
    except:
        prochaine_arborescence = PROCHAINES_ARBORESCENCE.get(prochaine_arborescence)
        st.session_state["arborescence"] = Arborescence(
            arborescence=prochaine_arborescence, num_question=1
        )
    st.session_state["select_option"] = None
    st.session_state['annee'] =  int(st.session_state.arborescence.question.annee)
    st.session_state["prochaine_arborescence"] = PROCHAINES_ARBORESCENCE.get(
        prochaine_arborescence
    )
    # Création des objets de l'arborescence
    init_objets(FICHIERS_OBJETS[prochaine_arborescence])
    init_programmes(FICHIERS_PROGRAMMES[prochaine_arborescence])
    # Mise à jour des objets depuis SQL
    update_indicateurs()
