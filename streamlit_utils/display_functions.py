"""
Fonctions pour afficher des données
"""
from datetime import datetime
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
EFFET_IMMEDIAT_DESC: str = "Effets immédiats"
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
    RENS: "Renseignement",
    COUT_UNITAIRE: "Coût unitaire",
    COUT_FIXE: "Coût fixe",
    COUT: "Coût du programme par année",
    ANNEE: "Année de disponibilité",
    UNITE_PAR_AN: "Cadence de production (unité/an)",
    DUREE: "Durée du programme",
    NOMBRE_UNITE: "Nombre d'unités",
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

def display_objet(objet_dict: dict, modification_objet: dict = {}, key: str = ""):
    st.subheader(f":blue[{objet_dict[NOM]}]")
    # Prix
    columns = st.columns(2)
    for i, compteur in enumerate([COUT_UNITAIRE, COUT_FIXE]):
        columns[i].metric(
            label=LABELS[compteur],
            value=objet_dict.get(compteur, 0) + modification_objet.get(compteur, 0),
            delta=modification_objet.get(compteur, 0),
        )
    columns[0].write(f"+-{objet_dict[STD_COUT]}€")
    # Effet sur les indicateurs
    modifications_indicateurs = {
        key: modification_objet.get(key)
        for key in [EUROPEANISATION, NIVEAU_TECHNO, BUDGET]
        if key in modification_objet.keys()
    }
    if len(modifications_indicateurs) > 0:
        st.subheader(f":blue[Effet par unité sur les compteurs]")
        display_metrics(modifications_indicateurs)
    # Bonus armées
    value_dict = {
        key: objet_dict.get(f"bonus_{key}", 0) for key in [AIR, MER, TERRE, RENS]
    }
    modification_dict = {
        key: modification_objet.get(f"bonus_{key}", 0)
        for key in [AIR, MER, TERRE, RENS]
    }
    fig = display_gauges_armees(
        values=value_dict, modifications=modification_dict, shape="bullet", grid=False
    )
    fig.update_layout(
        height=300,
        title=dict(
            text="Apport de chaque unité sur vos armées",
            font=dict(size=12, color="#333fff"),
        ),
        showlegend=True,
    )
    st.plotly_chart(fig, key=key)
    # Production
    unite_an = objet_dict.get(UNITE_PAR_AN, 0) + modification_objet.get(UNITE_PAR_AN, 0)
    disponibilié = objet_dict.get(ANNEE, 0) + modification_objet.get(ANNEE, 0)
    st.markdown(
        f"""
        :blue[Production]:\n
        Vous pourrez acheter jusqu'à **{unite_an}** unités par an à partir de l'année **{disponibilié}**
        """
    )


def display_programme(
    programme_dict: dict, modification_programme: dict = {}, key: str = ""
):
    st.subheader(f":blue[{programme_dict[NOM]}]")
    # Prix
    st.metric(
        label=LABELS[COUT],
        value=programme_dict.get(COUT, 0) + modification_programme.get(COUT, 0),
        delta=modification_programme.get(COUT, 0),
    )
    st.write(f"+-{programme_dict[STD_COUT]}€")
    st.metric(
        label=LABELS[DUREE],
        value=programme_dict.get(DUREE, 0) + modification_programme.get(DUREE, 0),
        delta=modification_programme.get(DUREE, 0),
    )
    # Effet sur les indicateurs
    modifications_indicateurs = {
        key: modification_programme.get(key)
        for key in [EUROPEANISATION, NIVEAU_TECHNO, BUDGET]
        if key in modification_programme.keys()
    }
    if len(modifications_indicateurs) > 0:
        st.subheader(f":blue[Effet par an sur les compteurs]")
        display_metrics(modifications_indicateurs)
    # Bonus armées
    # TODO


def display_objet_store(objet_dict: dict, key: str = ""):
    # Prix
    columns = st.columns(2)
    for i, compteur in enumerate([COUT_UNITAIRE, COUT_FIXE]):
        columns[i].metric(
            label=LABELS[compteur],
            value=objet_dict.get(compteur, 0),
        )
    # Bonus armées
    value_dict = {
        key: objet_dict.get(f"bonus_{key}", 0) for key in [AIR, MER, TERRE, RENS]
    }
    fig = display_gauges_armees(values=value_dict, grid=True)
    fig.update_layout(
        title=dict(
            text="Apport de chaque unité sur vos armées",
            font=dict(size=16, color="#333fff"),
        ),
        showlegend=True,
    )
    st.plotly_chart(fig, key=key)
    # Production
    unite_an = objet_dict.get(UNITE_PAR_AN, 0)
    st.markdown(
        f"""
        :blue[Cadence de production]: **{unite_an}** unités par an
        """
    )


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
            title=LABELS["bonus_" + armee],
            delta=reference,
            gauge=gauge_arg,
            domain={"row": i, "column": j},
        )
        return indicateur

    fig = go.Figure()

    if grid:
        for i, armee in enumerate([TERRE, AIR, MER, RENS]):
            if values.get(armee, 0) > 0:
                fig.add_trace(get_indicateur(armee, i // 2, i % 2))

        fig.update_layout(
            grid={"rows": 2, "columns": 2, "pattern": "independent"},
            margin=dict(l=50, r=50),
        )
    else:
        for i, armee in enumerate([TERRE, AIR, MER, RENS]):
            if values.get(armee, 0) > 0:
                fig.add_trace(get_indicateur(armee, i, 0))
        fig.update_layout(grid={"rows": 4, "columns": 1, "pattern": "independent"})
    return fig


def display_timeline(df, annee_courante, color, col_avancement=None):
    df[ANNEE] = annee_courante
    df["Pourcentage d'avancement"] = (annee_courante - df[DEBUT]) / (
        df[FIN] - df[DEBUT]
    )
    hover_template = {"Pourcentage d'avancement": ":.1%", ANNEE: True}
    if col_avancement:
        df[LABELS[col_avancement]] = df.apply(
            lambda x: str(x["Pourcentage d'avancement"] * x[col_avancement])
            + "/"
            + str(x[col_avancement]),
            axis=1,
        )
        hover_template[LABELS[col_avancement]] = True
    df[DEBUT] = df[DEBUT].apply(lambda x: datetime(year=x, month=1, day=1))
    df[FIN] = df[FIN].apply(lambda x: datetime(year=x, month=1, day=1))
    fig = px.timeline(
        df,
        x_start=DEBUT,
        x_end=FIN,
        y=color,
        color=color,
        hover_data=hover_template,
    )
    fig.update_yaxes(autorange="reversed")
    return fig
