"""
Fonctions pour afficher des données
"""
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import re
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

DRAPEAUX = {
    "France": "https://cdn.countryflags.com/thumbs/france/flag-400.png",
    "Allemagne": "https://cdn.countryflags.com/thumbs/germany/flag-400.png",
    "Angleterre": "https://cdn.countryflags.com/thumbs/united-kingdom/flag-400.png",
    "Italie": "https://cdn.countryflags.com/thumbs/italy/flag-400.png",
}
COLOR_MAP = {
    AIR: "#30b7d3",
    TERRE: "#59883a",
    MER: "#333fff",
    RENS: "#ff3a00",
}

###############
#   Fonction  #
###############

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


def display_objet(objet_dict: dict, modification_objet: dict, key: str = ""):
    value_dict = {
        key: objet_dict.get(f"bonus_{key}", 0) for key in [AIR, MER, TERRE, RENS]
    }
    modification_dict = {
        key: modification_objet.get(f"bonus_{key}", 0)
        for key in [AIR, MER, TERRE, RENS]
    }
    fig = display_gauges_armees(
        values=value_dict, modifications=modification_dict, shape="bullet", grid=True
    )
    st.plotly_chart(fig, key=key)
    st.dataframe(pd.DataFrame([objet_dict]))


def display_programme(programme_dict: dict):
    st.dataframe(pd.DataFrame([programme_dict]))


def display_annee():
    # TODO adapter en fonction des dates des arborecences
    percent_game = (st.session_state.annee - 1995) / (2050 - 1995)
    st.progress(percent_game, text=str(f"Année {st.session_state.annee}"))


def display_gauges_armees(values, modifications: dict = None, shape=None, grid=False):
    """
    Grid gauges
    """
    if modifications is not None:
        mode = "number+gauge+delta"
    else:
        mode = "number+gauge"
    gauge_arg = {"axis": {"visible": False}, "bar": {}}
    if shape is not None:
        gauge_arg["shape"] = shape

    def get_indicateur(armee, i, j):
        gauge_arg["bar"]["color"] = COLOR_MAP[armee]
        if modifications:
            reference = {"reference": values[armee]}
            values[armee] += modifications.get(armee, 0)
        else:
            reference = {}
        indicateur = go.Indicator(
            value=values[armee],
            mode=mode,
            title=LABELS[armee],
            delta=reference,
            gauge=gauge_arg,
            domain={"row": i, "column": j},
        )
        return indicateur

    fig = go.Figure()

    if grid:
        fig.add_trace(get_indicateur(TERRE, 0, 0))
        fig.add_trace(get_indicateur(MER, 1, 0))
        fig.add_trace(get_indicateur(AIR, 0, 1))
        fig.add_trace(get_indicateur(RENS, 1, 1))

        fig.update_layout(
            grid={"rows": 2, "columns": 2, "pattern": "independent"},
            margin=dict(l=50, r=50),
        )
    else:
        fig.add_trace(get_indicateur(TERRE, 0, 0))
        fig.add_trace(get_indicateur(MER, 1, 0))
        fig.add_trace(get_indicateur(AIR, 2, 0))
        fig.add_trace(get_indicateur(RENS, 3, 0))

        fig.update_layout(
            grid={"rows": 4, "columns": 1, "pattern": "independent"},
            margin=dict(l=50, r=50),
        )
    return fig
