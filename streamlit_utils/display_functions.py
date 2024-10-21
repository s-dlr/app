"""
Fonctions pour afficher des données
"""
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
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
    AIR: "Armée de l'air",
    TERRE: "Armée de terre",
    MER: "Marine",
    RENS: "Renseignement"
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


def display_objet(objet_dict: dict, key: str = ""):
    # fig = px.box(
    #     [
    #         objet_dict[COUT_UNITAIRE],
    #         objet_dict[COUT_UNITAIRE] - objet_dict[STD_COUT],
    #         objet_dict[COUT_UNITAIRE] + objet_dict[STD_COUT],
    #     ]
    # )
    # st.plotly_chart(fig, key=key)
    st.dataframe(pd.DataFrame([objet_dict]))


def display_programme(programme_dict: dict):
    st.dataframe(pd.DataFrame([programme_dict]))


def display_annee():
    # TODO adapter en fonction des dates des arborecences
    percent_game = (st.session_state.annee - 1995) / (2050 - 1995)
    st.progress(percent_game, text=str(f"Année {st.session_state.annee}"))

def display_gauges_armees(values):
    """
    Grid gauges
    """
    color_map = {
        AIR: "#30b7d3",
        TERRE: "#59883a",
        MER: "#333fff",
        RENS: "#ff3a00",
    }
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=values[TERRE],
            mode="gauge+number",
            title=LABELS[TERRE],
            gauge={"bar": {"color": color_map[TERRE]}},
            domain={"row": 0, "column": 0},
        )
    )
    fig.add_trace(
        go.Indicator(
            value=values[MER],
            mode="gauge+number",
            title=LABELS[MER],
            gauge={"bar": {"color": color_map[MER]}},
            domain={"row": 0, "column": 1},
        )
    )
    fig.add_trace(
        go.Indicator(
            value=values[AIR],
            mode="gauge+number",
            title=LABELS[AIR],
            gauge={"bar": {"color": color_map[AIR]}},
            domain={"row": 1, "column": 0},
        )
    )
    fig.add_trace(
        go.Indicator(
            value=values[RENS],
            mode="gauge+number",
            title=LABELS[RENS],
            gauge={"bar": {"color": color_map[RENS]}},
            domain={"row": 1, "column": 1},
        )
    )

    fig.update_layout(
        grid={"rows": 2, "columns": 2, "pattern": "independent"},
    )
    return fig
