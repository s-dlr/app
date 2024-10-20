"""
Fonctions pour afficher des données
"""
import pandas as pd
import streamlit as st

from src.variables import *

#############
#   Labels  #
#############

OBJET_DESC: str = "Objet concerné"
PROGRAMME_DESC: str = "Programme concerné"
EFFET_IMMEDIAT_DESC: str = "Effets immédiats sur vos compteurs"
LABELS: dict = {
    EUROPEANISATION: "Européanisation",
    NIVEAU_TECHNO: "Niveau technologique",
    BUDGET: "Budget",
    BONUS_AIR: "Bonus air",
    BONUS_MER: "Bonus mer",
    BONUS_RENS: "Bonus renseignement",
    BONUS_TERRE: "Bonus terre",
}


def display_metrics(effets_dict: dict):
    """
    Affiche des métriques
    """
    compteurs = st.session_state.indicateurs.to_dict()
    columns = st.columns(len(effets_dict))
    i = 0
    for compteur, effet in effets_dict.items():
        columns[i].metric(
            label=LABELS[compteur],
            value=compteurs.get(compteur, 0) + effet,
            delta=effet,
        )
        i += 1


def display_objet(objet_dict: dict):
    st.dataframe(pd.DataFrame([objet_dict]))


def display_programme(programme_dict: dict):
    st.dataframe(pd.DataFrame([programme_dict]))

def display_annee():
    # TODO adapter en fonction des dates des arborecences
    percent_game = (st.session_state.annee - 1995) / (2050 - 1995)
    st.progress(percent_game, text=str(f"Année {st.session_state.annee}"))
