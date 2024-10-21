from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

from src.variables import *
from streamlit_utils.display_functions import *

st.set_page_config(
    page_title="Dashboard",
    page_icon=":information_source:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

########################################################
################         SQL      ######################
########################################################

# Requêtes
QUERY_INDICATEURS = "SELECT * FROM `Indicateurs`"
QUERY_ARMEES = "SELECT * FROM `Armee`"
QUERY_DEPENDANCE = """
    SELECT UNIQUE equipe, dependance_export FROM Objets
    WHERE Objets.nom IN (SELECT objet FROM Constructions)
    UNION
    SELECT UNIQUE equipe, dependance_export FROM Programmes
    WHERE Programmes.debut IS NOT NULL AND dependance_export!=0;
"""
QUERY_PROGRAMMES = """
    SELECT equipe, nom, debut, fin, cout FROM Programmes
    WHERE Programmes.debut IS NOT NULL AND Programmes.debut != 0;
"""
QUERY_CONSTRUCTIONS = """
    SELECT equipe, objet, debut, fin, nombre_unites FROM Constructions
    WHERE Constructions.debut IS NOT NULL AND Constructions.debut != 0;
"""

# Connexion
dashboard_connection = st.connection("astrolabedb", autocommit=True, ttl=1)


########################################################
################       Equipes    ######################
########################################################

df_indicateurs = dashboard_connection.query(QUERY_INDICATEURS, ttl=5)
display_equipes = st.multiselect(
    'Equipes',
    df_indicateurs[EQUIPE].unique()
)
st.divider()


########################################################
################     Tables SQL   ######################
########################################################

# Données
df_armees = dashboard_connection.query(QUERY_ARMEES, ttl=5)
df_dependances = dashboard_connection.query(QUERY_DEPENDANCE, ttl=5)
df_dependances[DEPENDANCE_EXPORT] = df_dependances[DEPENDANCE_EXPORT].apply(
    lambda x: x.split(",")
)
df_dependances = df_dependances.explode(DEPENDANCE_EXPORT)
df_programmes = dashboard_connection.query(QUERY_PROGRAMMES, ttl=5)
df_constructions = dashboard_connection.query(QUERY_CONSTRUCTIONS, ttl=5)

########################################################
##############     Indicateurs macro   #################
########################################################

# Courbes indicateurs
col1, col2 = st.columns(2)
with col1:
    st.markdown(f":blue[Evolution des budgets]")
    st.line_chart(
        df_indicateurs[df_indicateurs[EQUIPE].isin(display_equipes)],
        x=ANNEE,
        y=BUDGET,
        color=EQUIPE,
    )

with col2:
    st.markdown(f":blue[Evolution des niveau technologiques]")
    st.line_chart(
        df_indicateurs[df_indicateurs[EQUIPE].isin(display_equipes)],
        x=ANNEE,
        y=NIVEAU_TECHNO,
        color=EQUIPE,
    )
st.divider()

########################################################
##############     Détail par équipe   #################
########################################################

# Affichage
for equipe, col in zip(display_equipes, st.columns(len(display_equipes))):
    with col.container(border=True):
        # Compteurs armées
        df_equipe = df_armees[df_armees[EQUIPE] == equipe]
        niveaux_armee = df_equipe.iloc[df_equipe[ANNEE].argmax()]
        col.markdown(f":blue[Armée de {equipe} en {df_equipe[ANNEE].max()}]")
        fig = display_gauges_armees(
            niveaux_armee[["terre", "air", "mer", "rens"]].to_dict()
        )
        col.plotly_chart(fig, use_container_width=True, key=f"gauge_terre_{equipe}")
        # Constructions
        df_constructions_equipe = df_constructions[df_constructions[EQUIPE] == equipe]
        df_constructions_equipe[OBJET] = df_constructions_equipe[OBJET].str.capitalize()
        fig = px.timeline(df_constructions_equipe, x_start=DEBUT, x_end=FIN, y=OBJET, color=OBJET)
        fig.update_layout(showlegend=False)
        fig.update_yaxes(autorange="reversed")
        col.plotly_chart(
            fig, use_container_width=True, key=f"constructions_{equipe}"
        ) 
        # Programmes
        df_programmes_equipe = df_programmes[df_programmes[EQUIPE] == equipe]
        df_programmes_equipe[NOM] = df_programmes_equipe[NOM].str.capitalize()
        fig = px.timeline(df_programmes_equipe, x_start=DEBUT, x_end=FIN, y=NOM, color=NOM)
        fig.update_layout(showlegend=False)
        fig.update_yaxes(autorange="reversed")
        col.plotly_chart(fig, use_container_width=True, key=f"programmes_{equipe}")
        # Dépendances
        col.markdown(f":blue[Dépendances de {equipe} en {df_indicateurs[ANNEE].max()}]")
        pays_dependance_equipe = (
            df_dependances[df_dependances[EQUIPE] == equipe][DEPENDANCE_EXPORT]
            .str.strip()
            .unique()
        )
        images_drapeaux = [
            DRAPEAUX.get(pays)
            for pays in pays_dependance_equipe
            if DRAPEAUX.get(pays) is not None
        ]
        df_indicateurs_equipe = df_indicateurs[df_indicateurs[EQUIPE] == equipe]
        col.metric(
            label=LABELS[EUROPEANISATION],
            value=df_indicateurs_equipe.iloc[df_indicateurs_equipe[ANNEE].argmax()][
                EUROPEANISATION
            ],
        )
        col.image(images_drapeaux, width=30)

# Lien vers les autres pages
st.page_link(
    "pages/store.py", label="Acheter des unités", icon=":material/shopping_cart:"
)
st.page_link("pages/options.py", label="Continuer", icon=":material/settings:")
