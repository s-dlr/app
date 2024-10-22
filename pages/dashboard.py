from datetime import datetime
import streamlit as st

from src.variables import *
from streamlit_utils.display_functions import *

st.set_page_config(
    page_title="Dashboard",
    page_icon=":material/dataset:",
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
df_last_info_equipe = df_indicateurs.sort_values(ANNEE, ascending=True)
df_last_info_equipe = df_indicateurs.drop_duplicates(EQUIPE, keep="last")
df_annee_equipe = df_indicateurs[[ANNEE, EQUIPE]].set_index(EQUIPE)
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
        annee_equipe = df_annee_equipe.loc[equipe]
        # Compteurs armées
        niveaux_armee = df_armees[
            (df_armees[EQUIPE] == equipe) & (df_armees[ANNEE] == annee_equipe)
        ].iloc[0]
        col.markdown(f":blue[Armée de {equipe} en {annee_equipe}]")
        fig = display_gauges_armees(
            niveaux_armee[["terre", "air", "mer", "rens"]].to_dict(), grid=True
        )
        col.plotly_chart(fig, use_container_width=True, key=f"gauge_terre_{equipe}")
        # Constructions
        df_constructions_equipe = df_constructions[df_constructions[EQUIPE] == equipe]
        fig = display_timeline(
            df_constructions_equipe,
            annee_courante=annee_equipe,
            col_avancement=NOMBRE_UNITE,
        )
        fig.update_layout(
            showlegend=False,
            title=dict(
                text="Achats en cours",
                font=dict(size=20),
            ),
        )
        col.plotly_chart(
            fig, use_container_width=True, key=f"constructions_{equipe}"
        ) 
        # Programmes
        df_programmes_equipe = df_programmes[df_programmes[EQUIPE] == equipe]
        fig = display_timeline(
            df_programmes_equipe,
            annee_courante=annee_equipe,
            col_avancement=NOMBRE_UNITE,
        )
        fig.update_layout(
            showlegend=False,
            title=dict(
                text="Programmes en cours",
                font=dict(size=20),
            ),
        )
        fig.update_yaxes(autorange="reversed")
        col.plotly_chart(fig, use_container_width=True, key=f"programmes_{equipe}")
        # Dépendances
        col.markdown(f":blue[Dépendances de {equipe} en {annee_equipe}]")
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
            value=df_last_info_equipe[EUROPEANISATION].iloc[0],
        )
        col.image(images_drapeaux, width=30)

# Lien vers les autres pages
st.page_link(
    "pages/store.py", label="Acheter des unités", icon=":material/shopping_cart:"
)
st.page_link("pages/options.py", label="Continuer", icon=":material/settings:")
